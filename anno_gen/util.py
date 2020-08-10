class NDArea:
    def __init__(self, dim):
        assert dim > 0
        self.dim = dim
        self.value = {}
        self._project = None

    def set(self, start, end, value):
        assert start < end
        self._project = None
        if self.dim > 1:
            assert isinstance(value, NDArea) and value.dim == self.dim - 1
        else:
            assert isinstance(value, bool)
        end_value = self.get(end)
        keys_to_remove = [i for i in self.value if start <= i <= end]
        for i in keys_to_remove:
            self.value.pop(i)
        if value != self.get(start):
            self.value[start] = value
        if value != end_value:
            self.value[end] = end_value
        
    def setall(self, value):
        self._project = None
        if self.dim == 1:
            assert all(isinstance(i, bool) for i in value.values())
        else:
            assert all(isinstance(i, NDArea) and i.dim == self.dim - 1 for i in value.values())
        indices = list(value)
        indices.sort()
        values = [self.zero] + [value[i] for i in indices]
        indices = [indices[i] for i in range(len(indices)) if values[i] != values[i+1]]
        self.value = {i: value[i] for i in indices}

    def remove_left(self, boundary):
        self._project = None
        value = self.get(boundary)
        keys_to_remove = [i for i in self.value if i <= boundary]
        for i in keys_to_remove:
            self.value.pop(i)
        if value != self.zero:
            self.value[boundary] = value

    def remove_right(self, boundary):
        self._project = None
        keys_to_remove = [i for i in self.value if i >= boundary]
        for i in keys_to_remove:
            self.value.pop(i)
        if self.get(boundary) != self.zero:
            self.value[boundary] = self.zero

    def get(self, x):
        possible_indices = [i for i in self.value if i <= x]
        if possible_indices:
            return self.value[max(possible_indices)]
        else:
            return self.zero

    def __eq__(self, other):
        return isinstance(other, NDArea) and self.dim == other.dim and self.value == other.value

    @property
    def area(self):
        if self.dim == 1:
            area = [(k, int(v)) for k, v in self.value.items()]
        else:
            area = [(k, v.area) for k, v in self.value.items()]
        if len(area) == 0:
            return 0
        area.sort()
        assert area[-1][1] == 0
        return sum(a[1]*(b[0]-a[0]) for a, b in zip(area[:-1], area[1:]))

    @property
    def zero(self):
        if self.dim == 1:
            return False
        else:
            return NDArea(self.dim - 1)

    def combine(self, other, op):
        assert isinstance(other, NDArea)
        assert self.dim == other.dim
        indices = set(self.value).union(set(other.value))
        indices = sorted(indices)
        if self.dim == 1:
            combine = {i: op(self.get(i), other.get(i)) for i in indices}
        else:
            combine = {i: self.get(i).combine(other.get(i), op) for i in indices}
        ret = NDArea(self.dim)
        ret.setall(combine)
        return ret

    def __add__(self, other):
        return self.combine(other, lambda x, y: x or y)

    def __sub__(self, other):
        return self.combine(other, lambda x, y: x and not y)

    def __mul__(self, other):
        return self.combine(other, lambda x, y: x and y)

    @property
    def project(self):
        if self._project is not None:
            return self._project
        ret = self.zero
        for k, v in self.value.items():
            ret = ret + v
        self._project = ret
        return ret

    @property
    def length(self):
        ret = max(self.value) - min(self.value)
        return ret


def rectangle(x0, y0, x1, y1):
    if x0 >= x1 or y0 >= y1:
        return NDArea(2)
    l = NDArea(1)
    l.set(y0, y1, True)
    r = NDArea(2)
    r.set(x0, x1, l)
    return r


def trajectory(traj, start_frame, end_frame):
    traj = {int(k): v for k, v in traj.items()}
    traj = {k: rectangle(*v) for k, v in traj.items()}
    ret = NDArea(3)
    ret.setall(traj)
    ret.remove_left(start_frame)
    ret.remove_right(end_frame+1)
    return ret
