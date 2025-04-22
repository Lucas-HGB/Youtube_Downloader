#!/usr/bin/env bash
cd backend && docker build -t youtube_downloader:api .
cd ..
cd frontend && docker build -t youtube_downloader:front .