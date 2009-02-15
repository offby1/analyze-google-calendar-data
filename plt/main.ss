#! /bin/sh
#| Hey Emacs, this is -*-scheme-*- code!
#$Id: v4-script-template.ss 5863 2008-12-21 17:13:36Z erich $
exec  mzscheme --require "$0" --main -- ${1+"$@"}
|#

#lang scheme

(require "google-auth.ss")

(provide main)
(define (main . args)
  (get-tokens))
