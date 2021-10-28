from textractcaller import call_textract
from trp import Document
import pytest
import logging
import os
import boto3


def test_get_full_json_from_file_and_bytes(caplog):
    caplog.set_level(logging.DEBUG, logger="textractcaller")
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(SCRIPT_DIR, "data/employmentapp.png")
    with open(input_file, "rb") as sample_file:
        b = bytearray(sample_file.read())
        j = call_textract(input_document=b)
        assert j
        doc = Document(j)
        assert doc

    with open(input_file, "rb") as sample_file:
        b = sample_file.read()
        j = call_textract(input_document=b)
        assert j
        doc = Document(j)
        assert doc


def test_tiff_sync(caplog):
    caplog.set_level(logging.DEBUG, logger="textractcaller")
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(SCRIPT_DIR, "data/employmentapp.tiff")
    j = call_textract(input_document=input_file)
    assert j
    assert 'Blocks' in j
    assert len(j['Blocks']) == 103
    doc = Document(j)
    assert doc


def test_tiff_async(caplog):
    caplog.set_level(logging.DEBUG, logger="textractcaller")
    textract_client = boto3.client('textract', region_name='us-east-2')
    input_file = os.path.join("s3://amazon-textract-public-content/blogs/employmentapp_20210510_compressed.tiff")
    j = call_textract(input_document=input_file, force_async_api=True, boto3_textract_client=textract_client)
    assert j
    assert 'Blocks' in j
    assert len(j['Blocks']) == 103
    doc = Document(j)
    assert doc


def test_tiff_async_multipage(caplog):
    caplog.set_level(logging.DEBUG, logger="textractcaller")
    textract_client = boto3.client('textract', region_name='us-east-2')
    input_file = os.path.join("s3://amazon-textract-public-content/blogs/multipage_tiff_example_small.tiff")
    j = call_textract(input_document=input_file, force_async_api=True, boto3_textract_client=textract_client)
    assert j
    assert 'Blocks' in j
    assert len(j['Blocks']) == 260
    doc = Document(j)
    assert doc


# multipage not supported on sync
def test_tiff_sync_multipage(caplog):
    caplog.set_level(logging.DEBUG, logger="textractcaller")
    textract_client = boto3.client('textract', region_name='us-east-2')
    input_file = os.path.join("s3://amazon-textract-public-content/blogs/multipage_tiff_example_small.tiff")
    with pytest.raises(textract_client.exceptions.UnsupportedDocumentException):
        call_textract(input_document=input_file, boto3_textract_client=textract_client)


def test_tiff_compressed_sync(caplog):
    caplog.set_level(logging.DEBUG, logger="textractcaller")
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(SCRIPT_DIR, "data/employmentapp.tiff")
    j = call_textract(input_document=input_file)
    assert j
    assert 'Blocks' in j
    assert len(j['Blocks']) == 103
    doc = Document(j)
    assert doc

    with open(input_file, "rb") as sample_file:
        b = bytearray(sample_file.read())
        j = call_textract(input_document=b)
        assert j
        assert 'Blocks' in j
        assert len(j['Blocks']) == 103
        doc = Document(j)
        assert doc
