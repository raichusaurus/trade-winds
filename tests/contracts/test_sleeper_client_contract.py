from __future__ import annotations

import pytest


@pytest.mark.contracts
def test_sleeper_client_get_user_by_username_returns_parsed_user_and_raw_payload(
    fixture_json,
) -> None:
    from trade_winds.sleeper.client import SleeperClient
    from trade_winds.sleeper.testing import FakeSleeperTransport

    payload = fixture_json("sleeper/user_seed.json")
    client = SleeperClient(
        base_url="https://api.sleeper.test/v1",
        transport=FakeSleeperTransport(
            {
                "/user/john_seed": payload,
            }
        ),
    )

    response = client.get_user_by_username("john_seed")

    assert response.user.user_id == "123456789"
    assert response.user.username == "john_seed"
    assert response.raw == payload


@pytest.mark.contracts
def test_sleeper_client_retries_transient_failures_before_success(fixture_json) -> None:
    from trade_winds.sleeper.client import SleeperClient
    from trade_winds.sleeper.testing import FakeSleeperTransport

    payload = fixture_json("sleeper/user_seed.json")
    transport = FakeSleeperTransport(
        {
            "/user/john_seed": [
                {"status_code": 503, "json": {"error": "try again"}},
                payload,
            ],
        }
    )
    client = SleeperClient(
        base_url="https://api.sleeper.test/v1",
        transport=transport,
        max_attempts=2,
    )

    response = client.get_user_by_username("john_seed")

    assert response.user.user_id == "123456789"
    assert transport.call_count("/user/john_seed") == 2


@pytest.mark.contracts
def test_sleeper_client_fetches_user_leagues_with_raw_payload(fixture_json) -> None:
    from trade_winds.sleeper.client import SleeperClient
    from trade_winds.sleeper.testing import FakeSleeperTransport

    payload = fixture_json("sleeper/user_leagues_current_season.json")
    client = SleeperClient(
        base_url="https://api.sleeper.test/v1",
        transport=FakeSleeperTransport({"/user/123456789/leagues/nfl/2026": payload}),
    )

    response = client.get_user_leagues("123456789", season=2026)

    assert response.raw == payload
    assert response.leagues[0].league_id == "league-1"
    assert response.leagues[0].season == 2026


@pytest.mark.contracts
def test_sleeper_client_fetches_league_users_and_rosters(fixture_json) -> None:
    from trade_winds.sleeper.client import SleeperClient
    from trade_winds.sleeper.testing import FakeSleeperTransport

    users_payload = fixture_json("sleeper/league_users.json")
    rosters_payload = fixture_json("sleeper/league_rosters.json")
    client = SleeperClient(
        base_url="https://api.sleeper.test/v1",
        transport=FakeSleeperTransport(
            {
                "/league/league-1/users": users_payload,
                "/league/league-1/rosters": rosters_payload,
            }
        ),
    )

    users_response = client.get_league_users("league-1")
    rosters_response = client.get_league_rosters("league-1")

    assert users_response.raw == users_payload
    assert [user.user_id for user in users_response.users] == [
        "123456789",
        "user-2",
        "user-3",
    ]
    assert rosters_response.raw == rosters_payload
    assert rosters_response.rosters[0].roster_id == 1
    assert rosters_response.rosters[0].owner_id == "123456789"


@pytest.mark.contracts
def test_sleeper_client_fetches_transactions_and_traded_picks(fixture_json) -> None:
    from trade_winds.sleeper.client import SleeperClient
    from trade_winds.sleeper.testing import FakeSleeperTransport

    transactions_payload = [
        fixture_json("sleeper/transactions_completed_trade.json"),
        fixture_json("sleeper/transactions_add_drop.json"),
    ]
    picks_payload = fixture_json("sleeper/traded_picks.json")
    client = SleeperClient(
        base_url="https://api.sleeper.test/v1",
        transport=FakeSleeperTransport(
            {
                "/league/league-1/transactions/2026": transactions_payload,
                "/league/league-1/traded_picks": picks_payload,
            }
        ),
    )

    transactions_response = client.get_league_transactions("league-1", season=2026)
    picks_response = client.get_traded_picks("league-1")

    assert transactions_response.raw == transactions_payload
    assert [transaction.transaction_id for transaction in transactions_response.transactions] == [
        "txn-trade-1",
        "txn-add-drop-1",
    ]
    assert picks_response.raw == picks_payload
    assert picks_response.traded_picks[0].season == 2027
    assert picks_response.traded_picks[0].round == 1


@pytest.mark.contracts
def test_sleeper_client_fetches_player_metadata_snapshot(fixture_json) -> None:
    from trade_winds.sleeper.client import SleeperClient
    from trade_winds.sleeper.testing import FakeSleeperTransport

    payload = fixture_json("sleeper/players.json")
    client = SleeperClient(
        base_url="https://api.sleeper.test/v1",
        transport=FakeSleeperTransport({"/players/nfl": payload}),
    )

    response = client.get_players()

    assert response.raw == payload
    assert response.players["4046"].full_name == "Bijan Robinson"
    assert response.players["4046"].position == "RB"


@pytest.mark.contracts
def test_sleeper_client_maps_not_found_to_controlled_error() -> None:
    from trade_winds.sleeper.client import SleeperClient
    from trade_winds.sleeper.errors import SleeperNotFoundError
    from trade_winds.sleeper.testing import FakeSleeperTransport

    client = SleeperClient(
        base_url="https://api.sleeper.test/v1",
        transport=FakeSleeperTransport(
            {"/user/missing_user": {"status_code": 404, "json": {"error": "not found"}}}
        ),
    )

    with pytest.raises(SleeperNotFoundError, match="missing_user"):
        client.get_user_by_username("missing_user")
