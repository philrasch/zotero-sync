from zotero_sync import __version__
from zotero_sync.__main__ import cli
from click.testing import CliRunner
from PyPDF2 import PdfFileWriter
import pytest
import uuid

runner = CliRunner()
ZOTFILE_DIR = 'data'
USER_ID = '6821801'
API_KEY = 'eZReAnu90cENprEbrVkW1oYO'


def get_num_files(data_dir):
    return len(list(data_dir.glob("**/*.pdf")))


def test_version():
    assert __version__ == '0.1.6'


@pytest.fixture(scope="function")
def data_dir(tmp_path_factory):
    pdf_writer = PdfFileWriter()
    pdf_writer.addBlankPage(width=72, height=72)
    data = tmp_path_factory.mktemp("data")
    for folder in range(2):
        parent = (data / str(folder))
        parent.mkdir(parents=True)
        for name in range(1):
            with (
                parent / f"{str(uuid.uuid4())}.pdf"
                ).open(mode='wb') as output_file:
                pdf_writer.write(output_file)
    return data


def test_optimize(data_dir):
    num_files = get_num_files(data_dir)
    result = runner.invoke(
        cli,
        [
            'optimize',
            '--file_dir', data_dir,
        ])
    assert result.exit_code == 0
    assert f"Finished Processing {num_files} files!" in result.output
    assert "Optimizing files" in result.output
    assert get_num_files(data_dir) == num_files


def test_ocr(data_dir):
    result = runner.invoke(
        cli,
        [
            'ocr',
            '--file_dir', data_dir
        ])
    assert result.exit_code == 0


def test_trash(data_dir):
    num_files = get_num_files(data_dir)
    result = runner.invoke(
        cli,
        [
            '--file_dir', data_dir,
            '--api_key', API_KEY,
            '--user_id', USER_ID,
            'trash'
        ])
    print(result.output)
    assert get_num_files(data_dir / "trash") == num_files
    assert result.exit_code == 0
    assert get_num_files(data_dir) == num_files
