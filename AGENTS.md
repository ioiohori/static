# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## プロジェクト概要

テイト・コーポレーション（TATE Corporation）の公式ホームページ。イベント企画・制作・招聘事業の静的Webサイト。
ビルドツールやフレームワークは使用せず、HTML/CSS/JSを直接編集してデプロイする。

## デプロイ

- Microsoft IIS上にファイルを配置する静的サイト（ビルドステップなし）
- 本番ドメイン: www.tate.jp

## アーキテクチャ

- **静的HTML構成**: 各ページが独立したHTMLファイル。テンプレートエンジンやSSGは未使用
- **CSS**: `css2019.css`（メイン）と `style.css`（サブ）の2ファイル構成。レスポンシブ対応（max-width: 1200px）
- **外部ライブラリ**: すべてCDN経由（Swiper JS、Meyer Reset CSS）
- **メール送信**: `php/` および `contact/postmail/` 配下のPHPスクリプト
- **外部連携**: Google Analytics (UA-130254129-1)、Facebook Page Plugin、YouTube Embed、MyTicket Navi

## ディレクトリ構成の要点

| ディレクトリ | 内容 |
|-------------|------|
| `concert/` | レガシーコンサート情報ページ |
| `concert2020/` | 2020年以降のコンサート情報（現行） |
| `company tate/` | 企業情報・アーティスト・プロデューサー紹介 |
| `index/` | トップページ用の画像・バナー・PDF資料 |
| `headernavi/` | ロゴ・favicon・ナビゲーション画像 |
| `contact/`, `kontact/` | お問い合わせフォーム（旧・新） |
| `_requests/` | クライアントからの更新要件（Git未追跡） |

## 作業パターン

- コンテンツ更新が主な作業（コンサート情報追加、バナー差し替え、ニュース更新）
- 新規コンサートページは `concert2020/` 配下に作成
- 画像・PDFは `index/` または各コンサートディレクトリに配置
- `.gitignore` で `*.mp4` を除外済み（動画ファイルはGit管理外）

## 注意事項

- ディレクトリ名にスペースを含むもの（`company tate/`）があるため、パス指定時は引用符が必要
- HTMLファイルごとにヘッダー・フッターを個別に持つため、共通部分の変更は全ファイルに反映が必要
- 日本語サイトのため、文字コードはUTF-8を維持すること
