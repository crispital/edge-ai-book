# 2.6与2.7仓库范围重置 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将克隆仓库整理为仅服务2.6和2.7的独立仓库，并把唯一远程改为`https://github.com/crispital/edge-ai-book.git`。

**Architecture:** 保留现有Git历史和通用规范，在当前工作树删除旧任务产物，统一重写任务入口与目录说明，再建立清理后的本地`main`基线。远程配置只保留新`origin`，不建立Fork、`upstream`或回合并关系。

**Tech Stack:** Git、PowerShell、Markdown、JSONL。

**Spec:** `docs/scope-reset-2.6-2.7-design.md`

## Global Constraints

- 当前活动范围只包含2.6“计算图、算子与模型结构”和2.7“PyTorch模型导出ONNX”。
- 删除只作用于当前工作树，不重写Git历史。
- 不使用Fork，不保留旧仓库远程，不计划回合并。
- 唯一远程为`https://github.com/crispital/edge-ai-book.git`。
- 完整数据、权重、ONNX、缓存和凭据不得进入Git。
- 本次不生成正文、实验结果、模型文件或虚构审核记录。
- 提交前检查完整差异；本计划不授权网络推送。

## Review Focus

- 删除路径必须全部位于`F:\edge-ai-book\d2el`且属于旧任务，通用规范不得误删。
- 清理后不得残留把2.8、2.9、4.1或旧3.x列为当前职责的入口。
- 保留的Markdown链接不得指向已删除文件。
- `.gitignore`必须继续排除数据、权重、ONNX、缓存和本地配置。
- 远程列表只能包含新`origin`，且不得执行`git push`。

---

### Task 1: 固定实施前基线

**Files:**
- Read: `AGENTS.md`
- Read: `第一阶段/docs/SPEC.md`
- Read: `docs/README.md`
- Read: `docs/repository-layout.md`
- Read: `CONTRIBUTING.md`
- Read: `docs/scope-reset-2.6-2.7-design.md`

**Interfaces:**
- Consumes: 用户批准的删除范围与唯一远程地址。
- Produces: 可恢复的清理前Git状态记录。

- [ ] **Step 1: 检查工作树和当前远程**

Run:

```powershell
git status --short --branch
git remote -v
git log -1 --oneline
```

Expected: 只有已批准的设计和计划文件为新增文件；没有其他用户改动。

- [ ] **Step 2: 保存明确的跟踪文件清单**

Run: `git ls-files`

Expected: 清单包含计划删除的2.8、2.9、4.1和旧3.x文件，可用于删除后复核。

### Task 2: 删除退出范围的工作产物

**Files:**
- Delete: `docs/ch02/02-08-*`
- Delete: `docs/ch02/02-09-*`
- Delete: `docs/references/ch02/ai-records/A-TASK-20261015-01/`
- Delete: `docs/ch04/`
- Delete: `docs/references/ch04/`
- Delete: `assets/ch04/`
- Delete: `reports/ch04/`
- Delete: `04-lightweight/`
- Delete: `docs/references/ch03/`
- Delete: `docs/first-week-2026-10-11.md`
- Delete: `docs/source-audit-2026-10-11.md`
- Delete: `docs/developer-guide.html`
- Delete: `02-onnx-baseline/configs/linux-autodl-train.example.json`
- Delete: `02-onnx-baseline/configs/windows-cpu-test.example.json`
- Replace: `docs/logs/2026/10/2026-10-15.jsonl`
- Replace: `docs/logs/2026/10/2026-10-15.md`
- Delete: other tracked `docs/logs/2026/10/2026-10-11*`

**Interfaces:**
- Consumes: Task 1跟踪文件清单。
- Produces: 不再包含旧任务稿、工作记录和AI输出的工作树。

- [ ] **Step 1: 用显式路径删除旧任务文件**

使用`git rm`逐个传入上述已核对路径，不使用未验证的递归变量、仓库根路径或跨Shell拼接。

- [ ] **Step 2: 验证删除范围**

Run: `git status --short` and `git diff --name-status`

Expected: 删除项全部属于本任务列出的旧任务范围，设计和计划文件保留。

### Task 3: 将单一事实入口改为2.6和2.7

**Files:**
- Modify: `第一阶段/docs/SPEC.md`
- Modify: `第一阶段/README.md`
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `CONTRIBUTING.md`
- Modify: `docs/README.md`
- Modify: `docs/current-tasks.md`
- Modify: `docs/repository-layout.md`
- Modify: `docs/records.md`
- Modify: `docs/cross-platform.md`
- Modify: `docs/ch02/README.md`
- Modify: `02-onnx-baseline/README.md`
- Modify: `assets/ch02/README.md`
- Modify: `reports/ch02/README.md`
- Modify: `datasets/README.md`
- Modify: `compatibility/README.md`
- Modify: `.gitignore`
- Modify: `.github/pull_request_template.md`

**Interfaces:**
- Consumes: `docs/scope-reset-2.6-2.7-design.md`中的范围和上传边界。
- Produces: 只把2.6和2.7列为当前职责的仓库规则与入口。

- [ ] **Step 1: 先重写个人SPEC**

SPEC只定义2.6和2.7的知识点、配套产出、边界及当前真实状态；删除原作者姓名、2.8、2.9、4.1和旧3.x职责。

- [ ] **Step 2: 同步规则和目录入口**

其余文件引用SPEC，不重复建立另一份范围事实；分支示例改为2.6和2.7，旧团队合并及旧远程说明删除。

- [ ] **Step 3: 保持上传边界**

`.gitignore`和目录说明继续排除完整MNIST数据、权重、ONNX、缓存、虚拟环境和本机配置；删除第四章白名单。

- [ ] **Step 4: 检查旧任务引用**

Run:

```powershell
rg -n "当前.*(2\.8|2\.9|4\.1|3\.1|3\.2|3\.3)|负责.*(2\.8|2\.9|4\.1|3\.1|3\.2|3\.3)|02-08|02-09|04-01|04-lightweight|docs/ch04|references/ch03|references/ch04" .
```

Expected: 没有活动规则或入口把退出章节列为当前工作；设计、计划和本次清理日志中的历史说明允许出现。

### Task 4: 更新本次真实工作记录

**Files:**
- Modify: `docs/logs/2026/10/2026-10-15.jsonl`
- Modify: `docs/logs/2026/10/2026-10-15.md`
- Read: `docs/schemas/work-event.schema.json`
- Read: `docs/logging-schema.md`

**Interfaces:**
- Consumes: Tasks 2—3的实际差异和检查结果。
- Produces: 仅记录本次范围重置事实的日志，不保留旧任务活动记录。

- [ ] **Step 1: 按schema写入范围重置事件**

记录用户确认、删除范围、保留范围、实际检查和未执行的推送；不伪造subagent、实验或审核事件。

- [ ] **Step 2: 生成对应Markdown摘要**

摘要只链接设计、计划、SPEC和实际Git检查，不复制旧任务内容。

- [ ] **Step 3: 验证JSONL逐行可解析**

Run:

```powershell
Get-Content docs/logs/2026/10/2026-10-15.jsonl | ForEach-Object { $_ | ConvertFrom-Json | Out-Null }
```

Expected: 命令退出码为0。

### Task 5: 完整性检查

**Files:**
- Check: all remaining tracked Markdown, JSON and JSONL files.

**Interfaces:**
- Consumes: Tasks 2—4的最终工作树。
- Produces: 可提交的清理差异。

- [ ] **Step 1: 检查已删除路径和保留路径**

Run: `git status --short`, `git diff --check`, `git diff --stat`, and `git diff --name-status`

Expected: 无空白错误；删除与修改范围符合设计。

- [ ] **Step 2: 检查链接和任务残留**

逐一核对根README、docs入口、目录README和SPEC中的相对链接；对`rg`命中的历史字样逐项判定，不以简单零命中代替人工检查。

- [ ] **Step 3: 检查不应入库的文件**

Run: `git status --short --ignored`

Expected: 数据、权重、ONNX、虚拟环境和缓存没有进入待提交文件。

### Task 6: 建立独立仓库本地基线

**Files:**
- Modify: local Git branch and remote configuration only.

**Interfaces:**
- Consumes: Task 5通过检查的工作树。
- Produces: 本地`main`基线和唯一新`origin`。

- [ ] **Step 1: 移除旧origin并添加新origin**

Run:

```powershell
git remote remove origin
git remote add origin https://github.com/crispital/edge-ai-book.git
git remote -v
```

Expected: 仅显示指向`crispital/edge-ai-book.git`的`origin`。

- [ ] **Step 2: 将当前本地分支重命名为main**

Run: `git branch -m main` and `git branch --show-current`

Expected: 输出`main`。

- [ ] **Step 3: 暂存并复核完整差异**

Run: `git add -A`, `git diff --cached --check`, `git diff --cached --stat`, and `git diff --cached`

Expected: 暂存区仅包含已批准的清理、规则同步、设计、计划和日志。

- [ ] **Step 4: 创建一个范围重置提交**

提交首行为：

```text
20261015 | 重置仓库范围为2.6与2.7
```

正文填写`CONTRIBUTING.md`规定的八项交稿说明，如实说明没有模型运行、没有外部审核、没有推送。

- [ ] **Step 5: 验证最终本地状态**

Run: `git status --short --branch`, `git remote -v`, and `git log -1 --format=fuller`

Expected: 本地`main`工作树干净，唯一远程为新`origin`，最新提交为范围重置；不执行`git push`。
