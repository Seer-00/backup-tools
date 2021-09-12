# backup.exe

```python
@Author: Seer    @Version: 0.2    @Last Updated: 2021.09.12
```

---

* **项目地址**：https://github.com/Seer-00/backup-tools
* **项目下载地址**(dev分支)：https://github.com/Seer-00/backup-tools/archive/refs/heads/dev.zip

| 版本号 |功能说明|更新日期| 备注 |
| ------ |---- |-------- | ---- |
| v0.1   | 程序基础结构，备份功能 | 2021.09.01 |      |
| v0.2 | 新增"忽略"选项 | 2021.09.12 |      |



#### 使用方法说明

* 首次运行*backup.exe*，自动生成*config.json*和logs文件夹
* 根据个人需求，编辑*config.json*
* 每次需要备份时，运行*backup.exe*
* 查看日志以获得运行结果
* **提示**
	* 可用**记事本查看和编辑** *config.json*和日志文件
	* *README.md* 和 *README.html* 内容一致
	* **[!!!] 程序的运行速度受备份的文件数量及文件大小影响**

#### <span id = "h-01">程序结构说明</span>
* 工作目录：用`.`表示，是*backup.exe*所处的文件夹。默认*config.json*和*README*均处于该目录下。
* <span id = "logs_path">日志目录</span>：默认为`./logs/`，用于存放日志。
* 日志文件：存放于日志目录，命名为：年月日-时分秒*.log*，记录程序每一次的运行情况。

---

#### 日志文件说明 

* 以下假定过程："将 A 备份至 B"

* 工作模式：
	1. **[默认] COPY**：当A备份至B以后，若A被删除，B仍存在
* 同名文件一致时：文件A, B具有**相同的文件名、大小和修改时间**
	1. **<span id="mode-skip">[默认] SKIP</span>**：跳过A至B的备份过程
* 同名文件更新时：文件A, B具有相同的文件名，但不满足前述条件，通常是A在上一次备份后进行了修改。
	1. **<span id='mode-overwrite'>[默认] OVERWRITE</span>**: 用A覆盖B

---

#### <span id = "h-02">Config文件说明</span>
* **在此设置程序的参数，该文件可重复使用**
* **所有路径必须已存在**，路径间用**逗号**分隔(**最后一个路径不要加逗号**)，路径分隔符可用 **\\** 或 **/ (推荐)**
* 文件名要带后缀，文件夹可以写成`D:/A`或`D:/A/`
* 参数说明
	* *backup_source*：备份源，需要备份的文件和文件夹。
	* *backup_ignore*：需要忽略的文件和文件夹。
	* *backup_destination*：备份目的地。
	* *logs_path*：对应[程序结构说明](#h-01)中的日志目录。

---
* config.json 示例一

	* 说明：将`D:/文件夹/`，备份至`E:/destination`，日志放在`D:/backup/logs/`


```json
{
    "backup_source": [
       "D:/文件夹/"
    ],
    "backup_ignore": [   
    ],
    "backup_destination": "E:/destination",
    "logs_path": "D:/backup/logs/"
}
```

* config.json 示例二

	* 说明：将文件夹`D:/A/`和文件`E:/B/b.txt`，备份至`D:/test/dst`，
	
		但忽略文件夹`D:/A/AA`和文件`D:/A/aa.jpg`，日志放在`D:/logs/`
```json
{
    "backup_source": [
       "D:/A/",
       "E:/B/b.txt"
    ],
    "backup_ignore": [
       "D:/A/AA",
       "D:/A/aa.jpg"
    ],
    "backup_destination": "D:/test/dst",
    "logs_path": "D:/logs/"
}
```


---

#### <span id = "h-03">日志标记说明</span>

| 标记     | 可能原因                       | 备注           |
| -------- | ------------------------------ | -------------- |
| [Begin]  | 正常，对应*config.json*的*backup_source* | 开始备份某源   |
| [Finish] | 正常，对应*config.json*的*backup_source* | 完成备份某源   |
| [Create] | 正常，目的地无对应文件夹          | 创建文件夹     |
| [Copy]   | 正常                           | 复制某文件(夹) |
| [Ignore] | 正常，对应*config.json*的*backup_ignore* | 忽略某文件(夹) |
| [Skip]   | 正常，[同名文件一致](#mode-skip)策略 | 跳过某文件(夹) |
| [OVERWRITE] | 正常，[同名文件更新](#mode-overwrite)策略 | 覆盖某文件(夹) |
| **[Redundant]** | **异常**，冗余的*source*路径或*ignore*路径 | e.g. *source*: "D:/A/", "D:/A/a.txt" |
| **[Conflict]** | **异常**，冲突的*source*和*ignore*路径 | e.g. *source*: "D:/A/a.txt", *ignore*: "D:/A/" |


---

#### Q&A

* **程序运行有无提示？**
目前程序运行所有状态（成功或异常）被记录在日志文件中，运行过程不输出任何提示。
* **如何根据个人需求编辑config.json？**
请参照[Config文件说明](#h-02)，并且不要破坏该文件的结构（如标点符号、关键字的名称等等）。
* **我删除了日志目录或日志文件，如何处理？**
这不会影响已完成的备份，但丢失了记录备份的信息。下次运行时，会自动创建新的日志目录和日志文件。
* **我删除了config.json，如何处理？**
这不会影响已完成的备份。但程序的运行依赖于config.json，下次运行时，将创建默认的config.json模板。
* **查看日志时发现异常信息，如何处理？**
请参照[日志标记说明](#h-03)，根据提示修正config.json。同时，日志中带有**[Finish]**标志的文件(夹)，表示已成功备份。
