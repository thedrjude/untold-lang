import pytest
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from stdlib.fs import UntoldFS as fs

class TestFS:
    def test_write_read(self, tmp_path):
        path = str(tmp_path / "test.txt")
        fs.write(path, "hello world")
        content = fs.read(path)
        assert content == "hello world"
    
    def test_append(self, tmp_path):
        path = str(tmp_path / "append.txt")
        fs.write(path, "start")
        fs.append(path, " end")
        assert fs.read(path) == "start end"
    
    def test_exists(self, tmp_path):
        path = str(tmp_path / "exists.txt")
        fs.write(path, "test")
        assert fs.exists(path) == True
        assert fs.exists("nonexistent.txt") == False
    
    def test_delete(self, tmp_path):
        path = str(tmp_path / "delete.txt")
        fs.write(path, "test")
        fs.delete(path)
        assert fs.exists(path) == False
    
    def test_mkdir(self, tmp_path):
        path = str(tmp_path / "newdir")
        fs.mkdir(path)
        assert os.path.isdir(path)
    
    def test_list_dir(self, tmp_path):
        path = str(tmp_path / "listdir")
        os.mkdir(path)
        open(f"{path}/file1.txt", "w").close()
        open(f"{path}/file2.txt", "w").close()
        files = fs.listdir(path)
        assert "file1.txt" in files
        assert "file2.txt" in files
    
    def test_copy(self, tmp_path):
        src = str(tmp_path / "src.txt")
        dst = str(tmp_path / "dst.txt")
        fs.write(src, "copy test")
        fs.copy(src, dst)
        assert fs.read(dst) == "copy test"
    
    def test_move(self, tmp_path):
        src = str(tmp_path / "src.txt")
        dst = str(tmp_path / "dst.txt")
        fs.write(src, "move test")
        fs.move(src, dst)
        assert fs.read(dst) == "move test"
        assert not os.path.exists(src)
    
    def test_size(self, tmp_path):
        path = str(tmp_path / "size.txt")
        fs.write(path, "12345")
        assert fs.size(path) == 5
    
    def test_json_write_read(self, tmp_path):
        path = str(tmp_path / "data.json")
        data = {"name": "test", "value": 42}
        fs.write_json(path, data)
        loaded = fs.read_json(path)
        assert loaded["name"] == "test"
        assert loaded["value"] == 42