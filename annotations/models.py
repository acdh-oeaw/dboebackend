from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
	"""Controlled vocabulary Class"""
	name = models.CharField(
		max_length=255,
		verbose_name="Name"
		)
	notation = models.CharField(
		max_length=200,
		blank=True,
		verbose_name="Notation"
		)
	note = models.TextField(
		blank=True,
		help_text="Note/Comment"
		)

	def __str__(self):
		return "{}".format(self.name)


class Es_document(models.Model):
	es_id = models.CharField(
		max_length=255,
		unique=True,
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
		related_name="collections",
		help_text="The user who created current collection"
		)
	es_document = models.ManyToManyField(
		Es_document,
		related_name="in_collections",
		verbose_name="Document",
		blank=True
		)
	public = models.BooleanField(
		default=False,
		help_text="Public collection or not. By default is not public."
		)
	comment = models.TextField(
		blank=True,
		help_text="Comment on collection"
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
		related_name="annotations",
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


