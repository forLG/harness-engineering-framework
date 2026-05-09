from qrwatch.cli import main


def test_cli_starts_in_dry_run_mode(capsys):
    assert main([]) == 0

    output = capsys.readouterr().out

    assert "QR Watch started in dry-run mode" in output
    assert "provider=dry-run" in output
    assert "capture=disabled" in output
    assert "notifications_sent=0" in output
