#!/usr/bin/env python
from __future__ import division
import numpy as np

def _augment(point):
  point = np.array(point,dtype=float,copy=True)
  s = np.shape(point) 
  a = np.ones(s[:-1]+(1,))
  return np.concatenate((point,a),axis=-1)

def _unaugment(point):
  point = np.array(point,dtype=float,copy=True)    
  return point[...,:-1]

class Transform:
  def __init__(self,M):
    M = np.asarray(M)
    self._M = M

  def __call__(self,point):
    point = _augment(point)
    out = np.einsum('ij,...j->...i',self._M,point)
    out = _unaugment(out) 
    return out

  def inverse(self):
    Minv = np.linalg.inv(self._M)
    return Transform(Minv)

  def get_M(self):
    return self._M
 
  def set_M(self,M):
    self._M = M

  def get_transformed_origin(self):
    return self._M[[0,1,2],3]

  def get_transformed_bases(self):
    return (self._M[[0,1,2],0],
            self._M[[0,1,2],1],
            self._M[[0,1,2],2])

  def then(self,other):
    ''' 
    combines transformation operations
    
    Example
    -------
      >>> RotateX = point_rotation_x(1.0)
      >>> RotateY = point_rotation_y(2.0)
      >>> TotalRotation = RotateX.then(RotateY)
    '''
    return Transform(other._M.dot(self._M))
      
  def __add__(self,other):
    return self.then(other)

  def __sub__(self,other):
    return self.then(other.inverse())


def identity():
  M = np.eye(4)
  return Transform(M)


def point_rotation_x(arg):
  M = np.array([[1.0, 0.0, 0.0, 0.0],
                [0.0, np.cos(arg), -np.sin(arg), 0.0],
                [0.0, np.sin(arg), np.cos(arg), 0.0],
                [0.0, 0.0, 0.0, 1.0]])
  return Transform(M)


def point_rotation_y(arg):
  M = np.array([[np.cos(arg), 0.0, np.sin(arg), 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [-np.sin(arg), 0.0, np.cos(arg), 0.0],
                [0.0, 0.0, 0.0, 1.0]])
  return Transform(M)


def point_rotation_z(arg):
  M = np.array([[np.cos(arg), -np.sin(arg), 0.0, 0.0],
                [np.sin(arg), np.cos(arg), 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]])
  return Transform(M)


def point_translation(T):  
  M = np.array([[1.0, 0.0, 0.0, T[0]],
                [0.0, 1.0, 0.0, T[1]],
                [0.0, 0.0, 1.0, T[2]],
                [0.0, 0.0, 0.0, 1.0]])
  return Transform(M)


def point_stretch(S):
  M = np.array([[S[0], 0.0, 0.0, 0.0],
                [0.0, S[1], 0.0, 0.0],
                [0.0, 0.0, S[2], 0.0],
                [0.0, 0.0, 0.0, 1.0]])
  return Transform(M)

def basis_rotation_x(arg):
  a = point_rotation_x(arg)
  return a.inverse()

def basis_rotation_y(arg):
  a = point_rotation_y(arg)
  return a.inverse()

def basis_rotation_z(arg):
  a = point_rotation_z(arg)
  return a.inverse()

def basis_translation(T):
  a = point_translation(T)
  return a.inverse()

def basis_stretch(S):
  a = point_stretch(S)
  return a.inverse()
