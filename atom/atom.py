class Atom:
    def __init__(self, symbol: str, x_pos: float, y_pos: float, z_pos: float) -> None:
        """
        constructor for creating a new element object
        :param symbol: elemental symbol
        :param x_pos: vector x-component of element
        :param y_pos: vector y-component of element
        :param z_pos: vector z-component of element
        """
        self.symbol = symbol
        self.x_pos = []
        self.x_pos.append(x_pos)
        self.y_pos = []
        self.y_pos.append(y_pos)
        self.z_pos = []
        self.z_pos.append(z_pos)
        self.length = 0

    def get_symbol(self) -> str:
        """
        :return: element symbol
        """
        return self.symbol

    def add_vector(self, x_pos: float, y_pos: float, z_pos: float) -> None:
        """
        adds a new vector this element object
        :param x_pos: vector x-component of element
        :param y_pos: vector y-component of element
        :param z_pos: vector z-component of element
        :return: None
        """
        self.x_pos.append(x_pos)
        self.y_pos.append(y_pos)
        self.z_pos.append(z_pos)
        self.length += 1

    def get_x_pos(self, index: int) -> float:
        """
        returns the x position of an element in the desired index
        :param index: desired index
        :return: vector x-component of the element in the desired index
        """
        return self.x_pos[index]

    def get_y_pos(self, index: int) -> float:
        """
        returns the x position of an element in the desired index
        :param index: desired index
        :return: vector y-component of the element in the desired index
        """
        return self.y_pos[index]

    def get_z_pos(self, index: int) -> float:
        """
        returns the x position of an element in the desired index
        :param index: desired index
        :return: vector z-component of the element in the desired index
        """
        return self.z_pos[index]

    def increment_size(self) -> None:
        """
        increments the amount of elements
        :return: None
        """
        self.length += 1

    def size(self) -> int:
        """
        returns the amount of elements
        :return: magnitude of the elements
        """
        return self.length
