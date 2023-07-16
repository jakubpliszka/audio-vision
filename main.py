import argparse

from src.core import Core


def parse_arguments() -> argparse.Namespace:
    # create the parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--user-api-key", help="Aspen API user api key", required=False, default=None)
    parser.add_argument("--tenant-id", help="Aspen API tenant ID", required=False, default=None)
    parser.add_argument("--server-ip-address", help="Aspen API server IP adress", required=False, default="localhost")
    parser.add_argument("--no-camera", help="Disable the camera", action="store_false", dest="use_camera")
    parser.add_argument("--no-aspen", help="Disable the Aspen connecton", action="store_false", dest="use_aspen")

    # parse the arguments
    args = parser.parse_args()

    # return the parsed arguments
    return args


def main():
    args = parse_arguments()
    print(args)
    core = Core(use_camera=args.use_camera, use_aspen=args.use_aspen, aspen_user_api_key=args.user_api_key,
                aspen_tenant_id=args.tenant_id, aspen_server_ip_address=args.server_ip_address)
    core.run()


if __name__ == "__main__":
    main()
