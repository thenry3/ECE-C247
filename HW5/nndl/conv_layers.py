import numpy as np
from nndl.layers import *
import pdb

""" 
This code was originally written for CS 231n at Stanford University
(cs231n.stanford.edu).  It has been modified in various areas for use in the
ECE 239AS class at UCLA.  This includes the descriptions of what code to
implement as well as some slight potential changes in variable names to be
consistent with class nomenclature.  We thank Justin Johnson & Serena Yeung for
permission to use this code.  To see the original version, please visit
cs231n.stanford.edu.  
"""

def conv_forward_naive(x, w, b, conv_param):
  """
  A naive implementation of the forward pass for a convolutional layer.

  The input consists of N data points, each with C channels, height H and width
  W. We convolve each input with F different filters, where each filter spans
  all C channels and has height HH and width HH.

  Input:
  - x: Input data of shape (N, C, H, W)
  - w: Filter weights of shape (F, C, HH, WW)
  - b: Biases, of shape (F,)
  - conv_param: A dictionary with the following keys:
    - 'stride': The number of pixels between adjacent receptive fields in the
      horizontal and vertical directions.
    - 'pad': The number of pixels that will be used to zero-pad the input.

  Returns a tuple of:
  - out: Output data, of shape (N, F, H', W') where H' and W' are given by
    H' = 1 + (H + 2 * pad - HH) / stride
    W' = 1 + (W + 2 * pad - WW) / stride
  - cache: (x, w, b, conv_param)
  """
  out = None
  pad = conv_param['pad']
  stride = conv_param['stride']

  # ================================================================ #
  # YOUR CODE HERE:
  #   Implement the forward pass of a convolutional neural network.
  #   Store the output as 'out'.
  #   Hint: to pad the array, you can use the function np.pad.
  # ================================================================ #
  
  N, C, H, W = x.shape
  F, _, HH, WW = w.shape

  H_out = 1 + (H + 2 * pad - HH) // stride
  W_out = 1 + (W + 2 * pad - WW) // stride

  out = np.zeros((N, F, H_out, W_out))

  xpad = np.pad(x, ((0,), (0,), (pad,), (pad,)), "constant", constant_values=(0,))


  for i in range(N):
    for j in range(F):
        for k in range(H_out):
            for l in range(W_out):
                section = xpad[i, :, k * stride:k * stride + HH, l * stride:l * stride + WW]
                out[i, j, k, l] = np.sum(section * w[j]) + b[j]

  # ================================================================ #
  # END YOUR CODE HERE
  # ================================================================ #
    
  cache = (x, w, b, conv_param)
  return out, cache


def conv_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a convolutional layer.

  Inputs:
  - dout: Upstream derivatives.
  - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

  Returns a tuple of:
  - dx: Gradient with respect to x
  - dw: Gradient with respect to w
  - db: Gradient with respect to b
  """
  dx, dw, db = None, None, None

  N, F, out_height, out_width = dout.shape
  x, w, b, conv_param = cache
  
  stride, pad = [conv_param['stride'], conv_param['pad']]
  xpad = np.pad(x, ((0,0), (0,0), (pad,pad), (pad,pad)), mode='constant')
  num_filts, _, f_height, f_width = w.shape

  # ================================================================ #
  # YOUR CODE HERE:
  #   Implement the backward pass of a convolutional neural network.
  #   Calculate the gradients: dx, dw, and db.
  # ================================================================ #

  db = np.zeros_like(b)
  dw = np.zeros_like(w)
  dx = np.zeros_like(x)
  dxpad = np.zeros_like(xpad)
    
  for i in range(N):
    for j in range(F):
        db[j] += np.sum(dout[i, j])
        
        for k in range(out_height):
            for l in range(out_width):
                dw[j] += xpad[i, :, k * stride:k * stride + f_height, l * stride:l * stride + f_width] * dout[i, j, k, l]
                dxpad[i, :, k * stride:k * stride + f_height, l * stride:l * stride + f_width] += w[j] * dout[i, j, k, l]
                
  dx = dxpad[:, :, pad:-pad, pad:-pad]
               
  # ================================================================ #
  # END YOUR CODE HERE
  # ================================================================ #

  return dx, dw, db


def max_pool_forward_naive(x, pool_param):
  """
  A naive implementation of the forward pass for a max pooling layer.

  Inputs:
  - x: Input data, of shape (N, C, H, W)
  - pool_param: dictionary with the following keys:
    - 'pool_height': The height of each pooling region
    - 'pool_width': The width of each pooling region
    - 'stride': The distance between adjacent pooling regions

  Returns a tuple of:
  - out: Output data
  - cache: (x, pool_param)
  """
  out = None
  
  # ================================================================ #
  # YOUR CODE HERE:
  #   Implement the max pooling forward pass.
  # ================================================================ #

  N, C, H, W = x.shape
    
  pool_height = pool_param["pool_height"]
  pool_width = pool_param["pool_width"]
  stride = pool_param["stride"]
  
  H_out = 1 + (H - pool_height) // stride
  W_out = 1 + (W - pool_width) // stride
    
  out = np.zeros((N, C, H_out, W_out))

  for i in range(N):
    for j in range(C):
      for k in range(H_out):
        for l in range(W_out):
            section = x[i, j, k * stride:k * stride + pool_height, l * stride:l * stride + pool_width]
            out[i, j, k, l] = np.max(section)
                
  # ================================================================ #
  # END YOUR CODE HERE
  # ================================================================ # 
  cache = (x, pool_param)
  return out, cache

def max_pool_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a max pooling layer.

  Inputs:
  - dout: Upstream derivatives
  - cache: A tuple of (x, pool_param) as in the forward pass.

  Returns:
  - dx: Gradient with respect to x
  """
  dx = None
  x, pool_param = cache
  pool_height, pool_width, stride = pool_param['pool_height'], pool_param['pool_width'], pool_param['stride']

  # ================================================================ #
  # YOUR CODE HERE:
  #   Implement the max pooling backward pass.
  # ================================================================ #
    
  N, C, H, W = x.shape
  _, _, H_out, W_out = dout.shape
    
  dx = np.zeros_like(x)
    
  for i in range(N):
    for j in range(C):
        for k in range(H_out):
            for l in range(W_out):
                section = x[i, j, k * stride:k * stride + pool_height, l * stride:l * stride + pool_width]
                
                max_val = np.max(section)
                mask = section == max_val
                
                dx[i, j, k * stride:k * stride + pool_height, l * stride:l * stride + pool_width] += dout[i, j, k, l] * mask

  # ================================================================ #
  # END YOUR CODE HERE
  # ================================================================ # 

  return dx

def spatial_batchnorm_forward(x, gamma, beta, bn_param):
  """
  Computes the forward pass for spatial batch normalization.
  
  Inputs:
  - x: Input data of shape (N, C, H, W)
  - gamma: Scale parameter, of shape (C,)
  - beta: Shift parameter, of shape (C,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance. momentum=0 means that
      old information is discarded completely at every time step, while
      momentum=1 means that new information is never incorporated. The
      default of momentum=0.9 should work well in most situations.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features
    
  Returns a tuple of:
  - out: Output data, of shape (N, C, H, W)
  - cache: Values needed for the backward pass
  """
  out, cache = None, None

  # ================================================================ #
  # YOUR CODE HERE:
  #   Implement the spatial batchnorm forward pass.
  #
  #   You may find it useful to use the batchnorm forward pass you 
  #   implemented in HW #4.
  # ================================================================ #
  
  mode = bn_param['mode']
  eps = bn_param.get('eps', 1e-5)
  momentum = bn_param.get('momentum', 0.9)
    
  N, C, H, W = x.shape
  x = x.reshape((N * H * W, C))
  _, D = x.shape

  running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
  running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

  if mode == "train":
    mean = np.mean(x, axis=0)
    variance = np.var(x, axis=0)
    x_norm = (x - mean) / np.sqrt(variance + eps)
    
    out = gamma * x_norm + beta
    
    running_mean = momentum * running_mean + (1 - momentum) * mean
    running_var = momentum * running_var + (1 - momentum) * variance
  elif mode == "test":
    x_norm = (x - running_mean) / np.sqrt(running_var + eps)
    out = gamma * x_norm + beta
  else:
    raise ValueError('Invalid forward batchnorm mode "%s"' % mode)
  
  bn_param['running_mean'] = running_mean
  bn_param['running_var'] = running_var

  out = out.reshape((N, C, H, W))
    
  cache = {
        "variance": variance,
        "x_norm": x_norm,
        "gamma": gamma,
        "beta": beta,
        "x_centralized": x - mean,
        "eps": eps
    }

  # ================================================================ #
  # END YOUR CODE HERE
  # ================================================================ # 

  return out, cache


def spatial_batchnorm_backward(dout, cache):
  """
  Computes the backward pass for spatial batch normalization.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, C, H, W)
  - cache: Values from the forward pass
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs, of shape (N, C, H, W)
  - dgamma: Gradient with respect to scale parameter, of shape (C,)
  - dbeta: Gradient with respect to shift parameter, of shape (C,)
  """
  dx, dgamma, dbeta = None, None, None

  # ================================================================ #
  # YOUR CODE HERE:
  #   Implement the spatial batchnorm backward pass.
  #
  #   You may find it useful to use the batchnorm forward pass you 
  #   implemented in HW #4.
  # ================================================================ #
  
  N_original, C, H, W = dout.shape
  dout = dout.reshape((N_original * W * H, C))
  N = dout.shape[0]

  x_norm = cache["x_norm"]
  gamma = cache["gamma"]
  variance = cache["variance"]
  x_centralized = cache["x_centralized"]
  eps = cache["eps"]

  dbeta = np.sum(dout, axis=0)
  dgamma = np.sum(dout * x_norm, axis=0)

  dx_norm = dout * gamma
  
  da = dx_norm / np.sqrt(variance + eps)
  
  dvardx = 2 * (x_centralized) / N
  dvar = -0.5 * np.sum(x_centralized * ((variance + eps) ** -1.5) * dx_norm, axis=0)
    
  du = -1 * np.sum(dx_norm, axis=0) / np.sqrt(variance + eps)

  dx = da + (dvardx * dvar) + (du / N)
  dx = dx.reshape((N_original, C, H, W))
    
  # ================================================================ #
  # END YOUR CODE HERE
  # ================================================================ # 

  return dx, dgamma, dbeta