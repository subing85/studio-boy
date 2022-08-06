import sys
import ast


def execute(**kwargs):
    from apis.media import pitcher

    output = pitcher.Connect.stamping(**kwargs)
    return True


if __name__ == "__main__":
    kwargs = ast.literal_eval(sys.argv[1])
    execute(**kwargs)
