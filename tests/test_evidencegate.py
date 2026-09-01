import pytest

from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded, tx_execution_failed


CONTRACT = "EvidenceGate.py"


def deploy():
    factory = get_contract_factory(contract_file_path=CONTRACT)
    return factory.deploy(args=[])


def test_initial_state():
    contract = deploy()

    assert contract.get_claim().call() == ""
    assert contract.get_evidence_url().call() == ""
    assert contract.get_verdict().call() == "NOT_EVALUATED"
    assert contract.get_reasoning().call() == ""
    assert contract.is_evaluated().call() is False


def test_create_claim():
    contract = deploy()

    tx = contract.create_claim(
        args=[
            "GenLayer Studio allows developers to build Intelligent Contracts",
            "https://docs.genlayer.com",
        ]
    ).transact()

    assert tx_execution_succeeded(tx)

    assert (
        contract.get_claim().call()
        == "GenLayer Studio allows developers to build Intelligent Contracts"
    )

    assert contract.get_evidence_url().call() == "https://docs.genlayer.com"


def test_empty_claim_rejected():
    contract = deploy()

    tx = contract.create_claim(
        args=["", "https://example.com"]
    ).transact()

    assert tx_execution_failed(tx)


def test_whitespace_claim_rejected():
    contract = deploy()

    tx = contract.create_claim(
        args=["   ", "https://example.com"]
    ).transact()

    assert tx_execution_failed(tx)


def test_empty_url_rejected():
    contract = deploy()

    tx = contract.create_claim(
        args=["A factual claim", ""]
    ).transact()

    assert tx_execution_failed(tx)


def test_invalid_url_scheme_rejected():
    contract = deploy()

    tx = contract.create_claim(
        args=["A factual claim", "ftp://example.com"]
    ).transact()

    assert tx_execution_failed(tx)


def test_duplicate_claim_rejected():
    contract = deploy()

    first_tx = contract.create_claim(
        args=["First claim", "https://example.com"]
    ).transact()

    assert tx_execution_succeeded(first_tx)

    second_tx = contract.create_claim(
        args=["Second claim", "https://example.org"]
    ).transact()

    assert tx_execution_failed(second_tx)


def test_evaluate_without_claim_rejected():
    contract = deploy()

    tx = contract.evaluate().transact()

    assert tx_execution_failed(tx)
