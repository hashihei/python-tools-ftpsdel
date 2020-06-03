# python-tools-ftpsdel
## Name
ftpsmdel
* FTPS環境で予めリストアップした複数のファイルを削除するスクリプトです。
　（後述するディレクトリリストとファイルリストに対し、たすき掛けでファイル削除を実施します。）

## Requirement
* python python3.x
    * 動作確認バージョンWindows(python 3.8.1)
* pytest (test only)

## Usage
* Windows Install (Use PowerShell)
```
git clone https://github.com/hashihei/python-tools-ftpsdel.git
```

* Configure
    1. etc/ftpdel.conf
        * [MUST]
            * FTP接続情報(HOST/USER/PASS/FTP_LOGIN_DIR)
                * FTP_LOGIN_DIRを設定するとログイン時に併せてサーバ側のカレントディレクトリを変更します。
        * [MAY]
            * FTP_DEL_LIST_DIR
                * 削除対象ファイルを探索するディレクトリのリスト を記載する設定ファイル
            * FTP_DEL_LIST_FILE 
                * 削除対象ファイル を記載する設定ファイル
    
    2. src/dirlist.txt
        * [MUST]
            * 削除対象ファイルを探索するディレクトリを指定(1行1項目、複数指定可能)

    3. src/filelist.txt
        * [MUST]
            * 削除対象ファイルを指定(1行1項目、複数指定可能)

* Execution
```
cd .\python-tools-ftpsdel\
ftpsmdel.py
```

* Execution Options
    * --config_file コンフィグファイルを指定しデフォルトから変更する
    * --start_index 指定した番号から削除を実行する。コマンドを中断した際、後から指定したindex番号から削除の再開が可能。index番号はデフォルトでは100番単位でログ及びプロンプトにprogressとして出力される。

## Author
hashihei

## Note
None.
