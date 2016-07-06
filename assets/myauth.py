#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Bob'
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

class UserProfileManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        #create and save a User with the given email,username and password

        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        #create and save a superuser with the given email,username and password

        user = self.create_user(
            email,
            password = password,
            username = username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser):
    email = models.EmailField(
        verbose_name = 'email address',
        unique=True,
        max_length=255,
    )
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    object = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self,app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin