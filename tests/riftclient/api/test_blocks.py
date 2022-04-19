import responses

from jumpclient import PortalClient


def test_all_calls_correct_url_with_default_params():
    responses.add(responses.GET, "http://127.0.0.1:4002/blocks", json={"success": True}, status=200)

    client = PortalClient("http://127.0.0.1:4002")
    client.blocks.all()
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "http://127.0.0.1:4002/blocks?limit=100"


def test_all_calls_correct_url_with_passed_in_params():
    responses.add(responses.GET, "http://127.0.0.1:4002/blocks", json={"success": True}, status=200)

    client = PortalClient("http://127.0.0.1:4002")
    client.blocks.all(page=5, limit=69)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url.startswith("http://127.0.0.1:4002/blocks?")
    assert "page=5" in responses.calls[0].request.url
    assert "limit=69" in responses.calls[0].request.url


def test_all_calls_correct_url_with_additional_params():
    responses.add(responses.GET, "http://127.0.0.1:4002/blocks", json={"success": True}, status=200)

    client = PortalClient("http://127.0.0.1:4002")
    client.blocks.all(page=5, limit=69, orderBy="timestamp.epoch", height=6838329)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url.startswith("http://127.0.0.1:4002/blocks?")
    assert "page=5" in responses.calls[0].request.url
    assert "limit=69" in responses.calls[0].request.url
    assert "orderBy=timestamp.epoch" in responses.calls[0].request.url
    assert "height=6838329" in responses.calls[0].request.url


def test_get_calls_correct_url():
    block_id = "12345"
    responses.add(
        responses.GET,
        "http://127.0.0.1:4002/blocks/{}".format(block_id),
        json={"success": True},
        status=200,
    )

    client = PortalClient("http://127.0.0.1:4002")
    client.blocks.get(block_id)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "http://127.0.0.1:4002/blocks/12345"


def test_first_calls_correct_url():
    responses.add(
        responses.GET, "http://127.0.0.1:4002/blocks/first", json={"success": True}, status=200
    )

    client = PortalClient("http://127.0.0.1:4002")
    client.blocks.first()

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "http://127.0.0.1:4002/blocks/first"


def test_last_calls_correct_url():
    responses.add(
        responses.GET, "http://127.0.0.1:4002/blocks/last", json={"success": True}, status=200
    )

    client = PortalClient("http://127.0.0.1:4002")
    client.blocks.last()

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "http://127.0.0.1:4002/blocks/last"


def test_transactions_calls_correct_url_with_default_params():
    block_id = "12345"
    responses.add(
        responses.GET,
        "http://127.0.0.1:4002/blocks/{}/transactions".format(block_id),
        json={"success": True},
        status=200,
    )

    client = PortalClient("http://127.0.0.1:4002")
    client.blocks.transactions(block_id)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == (
        "http://127.0.0.1:4002/blocks/12345/transactions?limit=100"
    )


def test_transactions_calls_correct_url_with_passed_in_params():
    block_id = "12345"
    responses.add(
        responses.GET,
        "http://127.0.0.1:4002/blocks/{}/transactions".format(block_id),
        json={"success": True},
        status=200,
    )

    client = PortalClient("http://127.0.0.1:4002")
    client.blocks.transactions(block_id, page=5, limit=69)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url.startswith(
        "http://127.0.0.1:4002/blocks/12345/transactions?"
    )
    assert "page=5" in responses.calls[0].request.url
    assert "limit=69" in responses.calls[0].request.url
