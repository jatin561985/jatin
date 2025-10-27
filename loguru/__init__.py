class _Logger:
    def info(self, message, *args):
        print(message % args if args else message)

    def warning(self, message, *args):
        print(message % args if args else message)

    def error(self, message, *args):
        print(message % args if args else message)

    def remove(self):
        pass

    def add(self, sink, level="INFO"):
        pass


logger = _Logger()
