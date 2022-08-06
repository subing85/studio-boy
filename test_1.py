class A1(object):

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):

        print("class a1")
        cls.output["path"] = "%s/jasmin/Modeling" % cls.input["root"]


class B1(A1):
    input = dict()

    @classmethod
    def execute(cls):
        super(B1, cls).execute()
        print("class B1")


if __name__ == "__main__":

    B1.input["root"] = "Z:/projects/RAR/assets"
    B1.execute()

    # print (B1.output)
