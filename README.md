# selfcitation

Finding Self Citations 

The devs in the dblp team were kind enough to provide a "library" and examples on how to use it.

[link](https://dblp.dagstuhl.de/faq/1474681.html)

first compile your java code in a class with :

```
	javac -cp mmdb-2019-04-29.jar codefilename.java
```

Then to run it, do:

```
	java -Xmx8G -cp mmdb-2019-04-29.jar:. codefilename /media/data6TB/Deshmukh/dblp.xml /media/data6TB/Deshmukh/dblp.dtd
```
