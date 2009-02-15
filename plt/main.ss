#! /bin/sh
#| Hey Emacs, this is -*-scheme-*- code!
#$Id: v4-script-template.ss 5863 2008-12-21 17:13:36Z erich $
exec  mzscheme --require "$0" --main -- ${1+"$@"}
|#

#lang scheme

(require "google-auth.ss")

;; Dig out a username and password from a file that happens to contain
;; that info.
(define (get-local-auth-info)
  (call-with-input-file (build-path (find-system-path 'home-dir) ".imap-authinfo")
    (lambda (ip)
      (let ((line (read-line ip)))
        (match line
          [(regexp #rx"login (.*?) password \"(.*)\"" (list _ username password))
           (values username password)])))))

(provide main)
(define (main . args)
  (call-with-values get-local-auth-info get-token))
