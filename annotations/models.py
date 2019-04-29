from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.db.models.signals import post_save, m2m_changed
from guardian.shortcuts import assign_perm, remove_perm
from django.dispatch import receiver
from django.db.models import Q
from django.contrib.postgres.fields import JSONField


class Category(models.Model):
	"""Controlled vocabulary Class"""
	name = models.CharField(
		max_length=255,
		verbose_name="Name"
		)
	description = models.TextField(
		blank=True,
		help_text="Describe the purpose of this category"
		)
	note = models.TextField(
		blank=True,
		help_text="Note/Comment"
		)
	notation = models.CharField(
		max_length=200,
		blank=True,
		verbose_name="Notation"
		)

	def __str__(self):
		return "{}".format(self.name)


class Tag(models.Model):
	"""Class to store tags for incoming elasticsearch documents"""
	name = models.CharField(
		max_length=255
		)
	color = models.CharField(
		max_length=255,
		blank=True
		)
	emoji = models.CharField(
		max_length=255,
		blank=True
		)
	meta = JSONField(
		null=True
		)

	def __str__(self):
		return self.name


class Es_document(models.Model):
	es_id = models.CharField(
		max_length=255,
		verbose_name="ID in elasticsearch index"
		)
	index = models.CharField(
		max_length=255,
		blank=True,
		verbose_name="Index"
		)
	version = models.IntegerField(
		blank=True,
		null=True,
		verbose_name="Version"
		)
	tag = models.ManyToManyField(
		Tag,
		related_name="es_documents",
		blank=True
		)

	def __str__(self):
		return "ID {}: {}".format(self.id, self.es_id)


class Collection(models.Model):
	"""1 to n references to elasticsearch documents"""
	title = models.CharField(
		max_length=255,
		blank=True,
		help_text="Title"
		)
	description = models.TextField(
		blank=True,
		help_text="Describe the collection",
		verbose_name="Description"
		)
	created_by = models.ForeignKey(
		User,
		blank=True, null=True,
		on_delete=models.SET_NULL,
		related_name="collections_created",
		help_text="The user who created current collection"
		)
	es_document = models.ManyToManyField(
		Es_document,
		related_name="in_collections",
		verbose_name="Document",
		blank=True
		)
	comment = models.TextField(
		blank=True,
		help_text="Comment on collection"
		)
	curator = models.ManyToManyField(
		User, related_name="collections_curated",
		blank=True,
		help_text="The selected user(s) will be able to view, edit and delete current Collection."
	)
	public = models.BooleanField(
		default=False,
		help_text="Public collection or not. By default is not public."
		)
	created = models.DateTimeField(editable=False, default=timezone.now)
	modified = models.DateTimeField(editable=False, default=timezone.now)


	def save(self, *args, **kwargs):
		if not self.id:
			self.created = timezone.now()
		self.modified = timezone.now()
		return super(Collection, self).save(*args, **kwargs)

	def __str__(self):
		if self.title:
			return "{}".format(self.title)
		else:
			return "{}".format(self.id)

	@property
	def tags(self):
		return set([tag for x in self.es_document.all() for tag in x.tag.all()])


class Annotation(models.Model):
	title = models.CharField(
		max_length=255,
		blank=True,
		verbose_name="Title"
		)
	collection = models.ForeignKey(
		Collection,
		on_delete=models.SET_NULL,
		related_name="annotations",
		verbose_name="Collection",
		blank=True, null=True
		)
	description = models.TextField(
		blank=True,
		help_text="Describe the annotation",
		verbose_name="Description"
		)
	category = models.ForeignKey(
		Category,
		on_delete=models.PROTECT,
		related_name="annotations",
		verbose_name="Category",
		blank=True, null=True
		)
	public = models.BooleanField(
		default=False,
		help_text="Public annotation or not. By default is not public."
		)
	created_by = models.ForeignKey(
		User,
		blank=True, null=True,
		on_delete=models.SET_NULL,
		related_name="annotations_created",
		help_text="The user who created current annotation"
		)
	created = models.DateTimeField(editable=False, default=timezone.now)
	modified = models.DateTimeField(editable=False, default=timezone.now)


	def save(self, *args, **kwargs):
		if not self.id:
			self.created = timezone.now()
		self.modified = timezone.now()
		return super(Annotation, self).save(*args, **kwargs)

	def __str__(self):
		return "{}".format(self.id)


#############################################################################
#
# Object Permissions on signals
#
#############################################################################

############## Adding Group 'general' with all Model Permissions ############

@receiver(post_save, sender=User, dispatch_uid="add_user_to_group")
def add_user_to_group(sender, instance=None, created=False, **kwargs):
	if created:
		g, _ = Group.objects.get_or_create(name='general')
		g.user_set.add(instance)
		# a new user has to have an access to view all public collections and their annotations
		for collection in Collection.objects.all():
			if collection.public is True:
				assign_perm('view_collection', instance, collection)
				if collection.annotations.all():
					for annotation in collection.annotations.all():
						assign_perm('view_annotation', instance, annotation)
			else:
				pass


@receiver(post_save, sender=Collection, dispatch_uid="create_perms_col_created_by")
def create_perms_col_created_by(sender, instance, **kwargs):
	assign_perm('delete_collection', instance.created_by, instance)
	assign_perm('change_collection', instance.created_by, instance)
	assign_perm('view_collection', instance.created_by, instance)
	if instance.public is True:
		for user in User.objects.exclude(username=instance.created_by):
			assign_perm('view_collection', user, instance)
			if instance.annotations.all():
				for annotation in instance.annotations.all():
					assign_perm('view_annotation', user, annotation)
	else:
		try:
			for user in User.objects.exclude(username=instance.created_by):
				if user not in instance.curator.all():
					remove_perm('view_collection', user, instance)
					if instance.annotations.all():
						for annotation in instance.annotations.all():
							remove_perm('view_annotation', user, annotation)
		except KeyError:
			pass
			


@receiver(post_save, sender=Annotation, dispatch_uid="create_perms_annotation_created_by")
def create_perms_annotation_created_by(sender, instance, **kwargs):
	assign_perm('delete_annotation', instance.created_by, instance)
	assign_perm('change_annotation', instance.created_by, instance)
	assign_perm('view_annotation', instance.created_by, instance)
	if instance.collection:
		if instance.collection.public is False:
			for curator in instance.collection.curator.all():
				assign_perm('delete_annotation', curator, instance)
				assign_perm('change_annotation', curator, instance)
				assign_perm('view_annotation', curator, instance)
				if curator is not instance.collection.created_by:
					assign_perm('delete_annotation', instance.collection.created_by, instance)
					assign_perm('change_annotation', instance.collection.created_by, instance)
					assign_perm('view_annotation', instance.collection.created_by, instance)
		else:
			for user in User.objects.all():
				if user in instance.collection.curator.all():
					assign_perm('delete_annotation', user, instance)
					assign_perm('change_annotation', user, instance)
					assign_perm('view_annotation', user, instance)
				elif user == instance.collection.created_by:
					assign_perm('delete_annotation', user, instance)
					assign_perm('change_annotation', user, instance)
					assign_perm('view_annotation', user, instance)
				else:
					assign_perm('view_annotation', user, instance)


################ Add/Remove a curator (user) to Collection ####################


@receiver(m2m_changed, sender=Collection.curator.through, dispatch_uid="create_perms_curator")
def create_perms_curator(sender, instance, **kwargs):
	if kwargs['action'] == 'pre_add':
		for curator in User.objects.filter(pk__in=kwargs['pk_set']):
			assign_perm('view_collection', curator, instance)
			assign_perm('change_collection', curator, instance)
			assign_perm('delete_collection', curator, instance)
			for obj in instance.annotations.all():
				assign_perm('view_'+obj.__class__.__name__.lower(), curator, obj)
				assign_perm('change_'+obj.__class__.__name__.lower(), curator, obj)
				assign_perm('delete_'+obj.__class__.__name__.lower(), curator, obj)
	elif kwargs['action'] == 'post_remove':
		for curator in User.objects.filter(pk__in=kwargs['pk_set']):
			# if Collection is public remove only change and delete perms but leave view perms for ex-curator
			if instance.public is True:
				#remove_perm('view_collection', curator, instance)
				remove_perm('change_collection', curator, instance)
				remove_perm('delete_collection', curator, instance)
				# if user removed from the curators list
				# he/she won't be able to access the objects he/she created within this Collection
				for obj in instance.annotations.all():
					#remove_perm('view_'+obj.__class__.__name__.lower(), curator, obj)
					remove_perm('change_'+obj.__class__.__name__.lower(), curator, obj)
					remove_perm('delete_'+obj.__class__.__name__.lower(), curator, obj)
			else:
				remove_perm('view_collection', curator, instance)
				remove_perm('change_collection', curator, instance)
				remove_perm('delete_collection', curator, instance)
				for obj in instance.annotations.all():
					remove_perm('view_'+obj.__class__.__name__.lower(), curator, obj)
					remove_perm('change_'+obj.__class__.__name__.lower(), curator, obj)
					remove_perm('delete_'+obj.__class__.__name__.lower(), curator, obj)
