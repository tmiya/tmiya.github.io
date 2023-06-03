# Fast Python

Manning Press の [Fast Python](https://www.manning.com/books/fast-python) を読んでのメモ。

jupyter notebook とかは [https://github.com/tiagoantao/python-performance](https://github.com/tiagoantao/python-performance) から `git clone` すれば自分の環境で動かせる。
（なお、環境も docker で用意されてる。）

## 1. An urgent need for efficiency in data processing

* 計算機の性能向上速度 (Moore's Law) より、解析すべきデータの量の増加速度 (Edholm's Law) の方が速い。
* データ量に合わせて計算機の予算を増やすのは無理。データ処理方法に工夫が必要になる。

----

* メモリ階層とアクセス速度の話。L1 cache(256kB, 2ns) から DIMM, SSD, HDD, cloud storage まで。
* ネットワークプロトコルの階層
* クラウドコンピューティング

----

### 1.3 Working with Python's limitations

* CPython
   * dynamic typing, garbage collection
   * 計算時間を要するような事柄は、CとかFortranで書かれた numpy の様なライブラリがやる
* The Global Interpreter Lock
   * CPython は基本的に同時に１スレッドしか動かない。  
      * Jython(JVM), IronPython(.NET) には GIL の制限は無い
   * concurrency と parallelism の違い
      * concurrency: IO 待ちを有効活用するための async 処理
   * GIL が問題になるような部分は低レベル言語で書かれたライブラリにやらせる。
   * multiprocessing なら GIL の問題は起きない。
   * この辺の話は chapter 3 で。

----

* Table 1.2: 各 chapter で扱う高速化手段

## 2. Extracting maximum performance from built-in features

### 2.1 Profiling applications with both IO and computing workloads

書籍ではコマンドラインでの実行が書かれているが、[chap_2_1.ipynb](./chap_2_1.ipynb) にnotebook上での profiling のやり方を示した。

* リモートファイルはローカルに cache すると速い。
   * しかし、リモートファイルが永遠に不変であるという保証が無いと、バグの原因となる。 

