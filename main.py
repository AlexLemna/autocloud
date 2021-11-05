import apis


def main():
    print("FOOBAR")
    cf = apis.Cloudflare()
    cf.verify_token(print_results=True)


if __name__ == "__main__":
    main()
