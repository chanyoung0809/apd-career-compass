@echo off
chcp 65001 >nul
title APD1 상담 입력 서버
cd /d "C:\KDT AX\APD1_OneOnOne"
echo ============================================
echo  APD1 1:1 상담 입력 서버를 시작합니다...
echo  브라우저가 자동으로 열립니다. (종료: 창 닫기 또는 Ctrl+C)
echo ============================================
python tools\상담_서버.py
pause
