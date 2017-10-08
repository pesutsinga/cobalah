class VPrinter:
    def __init__(self, verbose=True):
        self.verbose = verbose

    def vprint(self, obj):
        if self.verbose:
            print(obj)
