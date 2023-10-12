import math


def back_none():
    return None


class Tensor:
    """
    A custom tensor class that supports basic operations and automatic differentiation.

    Args:
        data (array-like): Input data to create the tensor.
        _parent (tuple, optional): Tuple of parent tensors in the computation graph. Defaults to ().
        _op (str, optional): Operation associated with this tensor. Defaults to ''.
        label (str, optional): Label or name for the tensor. Defaults to ''.
        req_grad (bool, optional): Whether gradient updates should be performed for this tensor. Defaults to False.

    Attributes:
        data (int): The underlying data stored in the tensor.
        label (str): A label for the tensor.
        grad (int): Gradient of the tensor with respect to some loss.
        req_grad (bool): Indicates if gradient updates are to be performed for this tensor.
    """

    def __init__(self, data, _parent=(), _op='', label='', req_grad=False):
        self.data = data
        self.label = label
        self.grad = 0
        self.req_grad = req_grad

        self._backward = back_none
        self._prev = set(_parent)
        self._op = _op

    # +++++++++++++++++ Basic Operations +++++++++++++++++

    def __add__(self, other) -> 'Tensor':
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data + other.data, (self, other), '+')

        def _backward():
            self.grad += 1 * out.grad
            other.grad += 1 * out.grad

        out._backward = _backward
        return out

    def __mul__(self, other) -> 'Tensor':
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data *out.grad
            other.grad += self.data *out.grad

        out._backward = _backward
        return out
    
    def __pow__(self, other) -> 'Tensor':
        assert isinstance(other, (int, float))
        out = Tensor(self.data ** other, (self, other), f'**{other}')
        
        def _backward():
            self.grad += (self.data**(other-1))*other * out.grad
        out._backward = _backward

        return out

    def __sub__(self, other) -> 'Tensor':
        return self + (-other)

    def __neg__(self) -> 'Tensor':
        return self * -1

    def __truediv__(self, other) -> 'Tensor':
        return self * (other ** -1)

    def __radd__(self, other) -> 'Tensor':
        return self + other

    def __rsub__(self, other) -> 'Tensor':
        return (-self) + other

    def __rmul__(self, other) -> 'Tensor':
        return self * other
    
    def __rtruediv__(self, other) -> 'Tensor':
        return other * (self ** -1)

    def __rpow__(self, other) -> 'Tensor':
        return other ** self

    # +++++++++++++++++ Basic Functions +++++++++++++++++

    def sin(self) -> 'Tensor':
        out = Tensor(math.sin(self.data), self)

        def _backward():
            self.grad += math.cos(self.data)*out.grad
        out._backward = _backward

        return out
    
    def cos(self) -> 'Tensor':
        out = Tensor(math.cos(self.data), self)

        def _backward():
            self.grad -= math.sin(self.data)*out.grad
        out._backward = _backward

        return out

    def exp(self) -> 'Tensor':
        out = Tensor(math.exp(self.data), self)
            
        def _backward():
            self.grad += math.exp(self.data)*out.grad
        out._backward = _backward

        return out

    def log(self) -> 'Tensor':
        out = Tensor(math.log(self.data), self)
            
        def _backward():
            self.grad += (1/self.data) * out.grad
        out._backward = _backward

        return out

    # +++++++++++++++++ Activation Functions +++++++++++++++++

    def relu(self) -> 'Tensor':
        out = Tensor(max(self.data, 0), self)

        def _backward():
            self.grad += (1 if self.data > 0 else 0) * out.grad

        out._backward = _backward
        return out

    def sigmoid(self) -> 'Tensor':
        sig = 1/(1+math.exp(-self.data))
        out = Tensor(sig, self)

        def _backward():
            self.grad += sig*(1-sig) *out.grad

        out._backward = _backward
        return out

    def tanh(self) -> 'Tensor':
        out = Tensor(math.tanh(self.data), self)

        def _backward():
            self.grad += (2*math.exp(self.data)/(math.exp(2*self.data)+1))**2

        out._backward = _backward
        return out

    # +++++++++++++++++ Loss Functions +++++++++++++++++

    def logistic_loss(self, target) -> 'Tensor':
        out = Tensor(math.sin(self.data), self)

        def _backward():
            self.grad += ... # your code here

        out._backward = _backward
        return out

    # +++++++++++++++++ Backward Pass and Optimization +++++++++++++++++

    def backward(self) -> None:
        topo = self._traverse_children()

        self.grad = 1
        for node in reversed(topo):
            node._backward()

    def zero_grad(self) -> None:
        topo = [self]
        topo.extend(self._traverse_children())

        for node in reversed(topo):
            node.grad = 0

    def step(self, learning_rate: float) -> None:
        topo = [self]
        topo.extend(self._traverse_children())

        for node in reversed(topo):
            if node.req_grad:
                node.data -= node.grad * learning_rate

    def _traverse_children(self) -> list:
        topo, visited = [], set()

        def build_topo(node):
            if node not in visited:
                visited.add(node)
                for child in node._prev:
                    build_topo(child)
                topo.append(node)

        build_topo(self)
        return topo

    def __repr__(self) -> str:
        return f'Tensor(data={self.data}, grad={self.grad}, label={self.label})'
