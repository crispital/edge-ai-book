# 仓库范围重置设计：仅保留2.6与2.7

日期：2026-10-15
状态：作者已确认

## 1. 目标与边界

将当前克隆仓库整理为后续自行维护的《端侧人工智能》工作仓库，当前工作范围仅包含：

- 2.6 计算图、算子与模型结构；
- 2.7 PyTorch模型导出ONNX。

本次整理只删除当前工作树中的旧任务文件并新增一次清理提交，不重写既有Git历史，不强制推送，也不操作旧仓库的任何远程分支。完整数据、权重和ONNX继续留在本地忽略目录，不纳入Git。

## 2. 删除范围

删除以下只服务于旧任务的跟踪内容：

- `docs/ch02/`中的2.8、2.9提纲和工作记录；
- `docs/references/ch02/ai-records/A-TASK-20261015-01/`；
- `docs/ch04/`、`docs/references/ch04/`、`assets/ch04/`、`reports/ch04/`；
- `04-lightweight/`；
- `docs/references/ch03/`中的旧3.x资料卡和AI记录；
- `docs/first-week-2026-10-11.md`、旧任务专属日志和旧任务来源核查记录；
- `docs/developer-guide.html`，避免继续维护包含旧任务范围的静态快照；
- `02-onnx-baseline/configs/`中仅面向旧2.8/4.1流程的示例配置。

删除操作通过Git记录，可从既有提交恢复；不清理对象库或历史提交。

## 3. 保留范围

保留并按新范围更新：

- 根目录管理文件：`AGENTS.md`、`README.md`、`CONTRIBUTING.md`、`.gitignore`、`.gitattributes`、`.editorconfig`和PR模板；
- 通用写作、记录、提示词、schema和跨平台规范；
- `02-onnx-baseline/`项目骨架；
- `docs/ch02/`、`docs/references/ch02/`、`assets/ch02/`和`reports/ch02/`入口；
- 与MNIST、ONNX结构和PyTorch导出直接相关且已登记来源的资料；
- `common/`、`datasets/`和`compatibility/`中仍适用于2.6、2.7的通用说明。

不会为2.6、2.7虚构正文、实验结果、ONNX文件或审核记录。新提纲、代码和实验记录在后续对应任务中按实际进度创建。

## 4. 同步修改

清理时同步更新以下单一事实入口，消除2.8、2.9、4.1及旧3.x活动任务引用：

- `第一阶段/docs/SPEC.md`与`第一阶段/README.md`；
- `AGENTS.md`、根`README.md`和`CHANGELOG.md`；
- `docs/current-tasks.md`、`docs/README.md`、`docs/repository-layout.md`；
- `CONTRIBUTING.md`中的当前章节、文件和分支示例；
- `docs/records.md`、`docs/cross-platform.md`及相关目录README；
- `.gitignore`中的目录白名单。

仓库启动流程仍为：每次任务先读`AGENTS.md`、个人SPEC和`docs/README.md`，再读任务对应规则并检查Git状态。

## 5. 远程仓库方案

本地唯一远程调整为：

- `origin`：`https://github.com/crispital/edge-ai-book.git`，作为后续自行维护和提交的唯一仓库。

不采用GitHub Fork关系，不保留`dixiLOG/d2el`的`upstream`远程，也不计划把后续工作合并回原仓库。原仓库地址只作为克隆来源事实记录在本次清理说明中，不再参与后续开发流程。

远程调整只修改本地Git配置，并用`git remote -v`核对本地配置。首次推送、设置默认分支或创建PR必须再次取得作者明确授权。

## 6. 分支与提交

当前清理先在本地形成差异并完成检查，再将当前分支改名为`main`，建立独立仓库的本地基线。本次不额外创建2.6或2.7功能分支。

清理完成后：

1. 检查删除清单、剩余旧任务引用、链接、`.gitignore`和工作树差异；
2. 按实际北京时间使用`YYYYMMDD | 中文事件`格式提交；
3. 在清理后的本地`main`创建一个范围重置提交；
4. 未获明确授权前不推送；后续实际开展单节任务时再创建对应功能分支。

## 7. 验收条件

- 活动任务入口只列2.6与2.7；
- 当前工作树不再包含2.8、2.9、4.1及旧3.x的任务稿、工作记录和AI输出；
- 通用规则与模板仍可使用，内部链接不存在已删除目标；
- `02-onnx-baseline/`保留且说明改为2.6、2.7；
- Git历史未被重写；
- 本地只保留第5节规定的新`origin`，没有`upstream`或指向原仓库的其他远程，也没有未经授权的推送；
- 检查结果只记录实际执行情况。
