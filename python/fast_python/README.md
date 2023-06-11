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

コマンドラインからのプロファイリングは、

```bash
$ python -m cProfile -s cumulative load.py 01044099999,02293099999 2021-2021
{'01044099999': -10.0, '02293099999': -27.6}
         382939 function calls (377391 primitive calls) in 38.255 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    137/1    0.000    0.000   38.255   38.255 {built-in method builtins.exec}
        1    0.000    0.000   38.255   38.255 load.py:1(<module>)
        1    0.001    0.001   38.060   38.060 load.py:27(download_all_data)
        2    0.000    0.000   38.059   19.030 load.py:17(download_data)
        2    0.000    0.000   38.044   19.022 api.py:62(get)
        2    0.000    0.000   38.044   19.022 api.py:14(request)
        2    0.000    0.000   38.040   19.020 sessions.py:500(request)
        2    0.000    0.000   38.032   19.016 sessions.py:671(send)
     2990    0.013    0.000   35.910    0.012 socket.py:691(readinto)
     2990    0.013    0.000   35.886    0.012 ssl.py:1263(recv_into)
     2990    0.009    0.000   35.871    0.012 ssl.py:1121(read)
     2990   35.861    0.012   35.861    0.012 {method 'read' of '_ssl._SSLSocket' objects}
        6    0.000    0.000   35.626    5.938 models.py:887(content)
       22    0.006    0.000   35.626    1.619 {method 'join' of 'bytes' objects}
     1171    0.002    0.000   35.620    0.030 models.py:812(generate)
     1171    0.005    0.000   35.618    0.030 response.py:607(stream)
     1169    0.023    0.000   35.611    0.030 response.py:535(read)
     1169    0.004    0.000   35.536    0.030 response.py:487(_fp_read)
     1169    0.013    0.000   35.532    0.030 client.py:450(read)
     1304    0.025    0.000   35.518    0.027 {method 'read' of '_io.BufferedReader' objects}
:
:
```

```
$ python -m cProfile -s cumulative load_cache.py 01044099999,02293099999 2021-2021
{'01044099999': -10.0, '02293099999': -27.6}
         308137 function calls (302709 primitive calls) in 0.165 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    135/1    0.000    0.000    0.165    0.165 {built-in method builtins.exec}
        1    0.000    0.000    0.165    0.165 load_cache.py:1(<module>)
       15    0.000    0.000    0.149    0.010 __init__.py:1(<module>)
        1    0.004    0.004    0.090    0.090 load_cache.py:51(get_all_temperatures)
    33650    0.076    0.000    0.084    0.000 load_cache.py:36(get_file_temperatures)
    180/3    0.000    0.000    0.075    0.025 <frozen importlib._bootstrap>:1022(_find_and_load)
    179/3    0.000    0.000    0.075    0.025 <frozen importlib._bootstrap>:987(_find_and_load_unlocked)
    165/3    0.000    0.000    0.075    0.025 <frozen importlib._bootstrap>:664(_load_unlocked)
    133/3    0.000    0.000    0.075    0.025 <frozen importlib._bootstrap_external>:877(exec_module)
    210/3    0.000    0.000    0.074    0.025 <frozen importlib._bootstrap>:233(_call_with_frames_removed)
    30/12    0.000    0.000    0.057    0.005 {built-in method builtins.__import__}
    70/41    0.000    0.000    0.042    0.001 <frozen importlib._bootstrap>:1053(_handle_fromlist)
        2    0.000    0.000    0.037    0.019 exceptions.py:1(<module>)
  179/143    0.001    0.000    0.029    0.000 <frozen importlib._bootstrap>:921(_find_spec)
 1817/672    0.000    0.000    0.021    0.000 {built-in method builtins.hasattr}
        4    0.000    0.000    0.021    0.005 six.py:117(_resolve)
        7    0.000    0.000    0.021    0.003 six.py:85(_import_module)
        1    0.000    0.000    0.020    0.020 connectionpool.py:1(<module>)
       18    0.000    0.000    0.020    0.001 six.py:190(find_spec)
        6    0.000    0.000    0.020    0.003 <frozen importlib._bootstrap>:421(spec_from_loader)
        4    0.000    0.000    0.020    0.005 six.py:215(is_package)
        1    0.000    0.000    0.020    0.020 six.py:120(__getattr__)
       76    0.000    0.000    0.019    0.000 re.py:288(_compile)
       75    0.000    0.000    0.019    0.000 re.py:249(compile)
        1    0.000    0.000    0.018    0.018 client.py:1(<module>)
       72    0.000    0.000    0.018    0.000 sre_compile.py:783(compile)
        2    0.000    0.000    0.017    0.009 connection.py:1(<module>)
        1    0.000    0.000    0.015    0.015 compat.py:1(<module>)
      133    0.000    0.000    0.013    0.000 <frozen importlib._bootstrap_external>:950(get_code)
  165/164    0.000    0.000    0.013    0.000 <frozen importlib._bootstrap>:564(module_from_spec)
        3    0.000    0.000    0.012    0.004 utils.py:1(<module>)
        1    0.000    0.000    0.012    0.012 ssl_.py:1(<module>)
       72    0.000    0.000    0.011    0.000 sre_parse.py:944(parse)
        1    0.000    0.000    0.011    0.011 parser.py:1(<module>)
   336/72    0.001    0.000    0.011    0.000 sre_parse.py:436(_parse_sub)
        1    0.000    0.000    0.011    0.011 feedparser.py:1(<module>)
    26/25    0.000    0.000    0.011    0.000 <frozen importlib._bootstrap_external>:1174(create_module)
   451/77    0.004    0.000    0.011    0.000 sre_parse.py:494(_parse)
    26/25    0.011    0.000    0.011    0.000 {built-in method _imp.create_dynamic}
      177    0.000    0.000    0.010    0.000 <frozen importlib._bootstrap_external>:1431(find_spec)
      177    0.000    0.000    0.010    0.000 <frozen importlib._bootstrap_external>:1399(_get_spec)
        1    0.000    0.000    0.010    0.010 _policybase.py:1(<module>)
        1    0.000    0.000    0.010    0.010 url.py:1(<module>)
  460/459    0.004    0.000    0.010    0.000 {built-in method builtins.__build_class__}
:
:
```

### Profiling code to detect performance bottlenecks

プロファイルは `-o` オプションでファイルに出力可能。
```
$ python -m cProfile -o distance_cache.prof distance_cache.py
```

その結果は、`snakeviz` コマンドでグラフィカルに確認可能。

```
$ pip install snakeviz
$ snakeviz distance_cache.prof
```

![snakeviz画像](fig_2_2_1.png)

