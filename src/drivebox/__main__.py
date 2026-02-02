from drivebox.app import App


def main() -> None:
    application = App()
    raise SystemExit(application.run())


if __name__ == "__main__":
    main()