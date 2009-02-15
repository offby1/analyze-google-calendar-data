#! /bin/sh
#| Hey Emacs, this is -*-scheme-*- code!
#$Id: v4-script-template.ss 5863 2008-12-21 17:13:36Z erich $
exec  mzscheme --require "$0" --main -- ${1+"$@"}
|#

#lang scheme

(include "eli.ss")

(define *auth-url* (string->url "https://www.google.com/accounts/ClientLogin"))

(provide main)
(define (main . args)
  (for ([line (in-lines (ssl:get-pure-port (string->url "https://google.com:443")))])
    (display line)
    (newline)))
