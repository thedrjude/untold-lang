import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from stdlib.fs import UntoldFS


class TestFS:
    def test_write_read(self, tmp_path):
        path = str(tmp_path / "test.txt")
        UntoldFS.write(path, "hello world")
        content = UntoldFS.read(path)
        assert content == "hello world"
    
    def test_append(self, tmp_path):
        path = str(tmp_path / "append.txt")
        UntoldFS.write(path, "start")
        UntoldFS.append(path, " end")
        assert UntoldFS.read(path) == "start end"
    
    def test_exists(self, tmp_path):
        path = str(tmp_path / "exists.txt")
        UntoldFS.write(path, "test")
        assert UntoldFS.exists(path) is True
        assert not UntoldFS.exists("nonexistent.txt")
    
    def test_delete(self, tmp_path):
        path = str(tmp_path / "delete.txt")
        UntoldFS.write(path, "test")
        UntoldFS.delete(path)
        assert not UntoldFS.exists(path)
    
    def test_mkdir(self, tmp_path):
        path = str(tmp_path / "newdir")
        UntoldFS.mkdir(path)
        assert os.path.isdir(path)
    
    def test_list_dir(self, tmp_path):
        path = str(tmp_path / "listdir")
        os.mkdir(path)
        open(f"{path}/file1.txt", "w").close()
        open(f"{path}/file2.txt", "w").close()
        files = UntoldFS.listdir(path)
        assert "file1.txt" in files
        assert "file2.txt" in files
    
    def test_copy(self, tmp_path):
        src = str(tmp_path / "src.txt")
        dst = str(tmp_path / "dst.txt")
        UntoldFS.write(src, "copy test")
        UntoldFS.copy(src, dst)
        assert UntoldFS.read(dst) == "copy test"
    
    def test_move(self, tmp_path):
        src = str(tmp_path / "src.txt")
        dst = str(tmp_path / "dst.txt")
        UntoldFS.write(src, "move test")
        UntoldFS.move(src, dst)
        assert UntoldFS.read(dst) == "move test"
        assert not os.path.exists(src)
    
    def test_size(self, tmp_path):
        path = str(tmp_path / "size.txt")
        UntoldFS.write(path, "12345")
        assert UntoldFS.size(path) == 5
    
    def test_json_write_read(self, tmp_path):
        path = str(tmp_path / "data.json")
        data = {"name": "test", "value": 42}
        UntoldFS.write_json(path, data)
        loaded = UntoldFS.read_json(path)
        assert loaded["name"] == "test"
        assert loaded["value"] == 42