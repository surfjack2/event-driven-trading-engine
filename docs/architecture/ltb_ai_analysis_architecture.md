# LTB AI Code Analysis Architecture

## Overview

LTB 프로젝트는 SonarQube와 Local LLM을 연계하여 코드 품질 분석 및 자동 문서화를 수행한다.


---

## System Architecture

Developer Code

↓

Git Repository

↓

SonarQube Analysis

↓

Code Quality Report

↓

LLM Analysis Layer

↓

Insights


---

## SonarQube 역할

Static Code Analysis

code smells
security issues
complexity


---

## LLM 역할

코드 설명 생성

architecture explanation

risk analysis


전략 코드 분석

strategy logic summary


취약점 분석

security review


---

## LLM Integration

Local LLM

Ollama
OpenCode
Claude Agent


---

## Example Workflow

Commit Code

↓

CI Pipeline

↓

SonarQube Scan

↓

LLM 분석

↓

자동 리포트 생성


---

## Expected Benefits

코드 품질 향상

자동 문서화

전략 코드 이해도 향상

보안 취약점 탐지
