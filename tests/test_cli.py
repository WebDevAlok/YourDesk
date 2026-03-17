from yourdesk.cli import build_parser


def test_parser_builds() -> None:
    parser = build_parser()
    args = parser.parse_args(["join", "--broker", "http://localhost:8080", "123-456-789"])
    assert args.code == "123-456-789"
