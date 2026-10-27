@echo off
REM ============================================================================
REM  IND 全数据集流水线 —— 唯一启动器（区域自带，2026-10-25）
REM
REM  并发固定 2（用户定稿）；十年数据硬要求（--require-ten-years）。
REM  只打未点亮塔优先的 7 个类别；断点/结果/digest/锁按 _IND 隔离，
REM  可与 EUR campaign 并行（平台账户级并发仍受全局限流约束）。
REM
REM  等价命令（Git Bash）：
REM    WQB_CAMPAIGN_REGION=IND WQB_REPO_ROOT=<repo> \
REM      <venv-python> -X utf8 ind_runner.py --only-cats ... --max-inflight 2
REM ============================================================================
setlocal
if not defined WQB_REPO_ROOT set WQB_REPO_ROOT=D:\coding\traeCN_project\wqb
set WQB_CAMPAIGN_REGION=IND
cd /d "%~dp0"

"%WQB_REPO_ROOT%\world-quant-brain-mcp\.venv\Scripts\python.exe" -X utf8 ind_runner.py ^
  --only-cats EARNINGS,IMBALANCE,INSIDERS,MACRO,OPTION,SENTIMENT,SHORTINTEREST ^
  --min-cov 0.35 --require-ten-years ^
  --max-inflight 2 --stall-sec 900 --check-sec 60 --zero-alpha-stop 3 ^
  >> "%WQB_REPO_ROOT%\logs\ind_runner.out" 2>&1

endlocal
