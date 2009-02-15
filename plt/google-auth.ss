#! /bin/sh
#| Hey Emacs, this is -*-scheme-*- code!
#$Id: v4-script-template.ss 5863 2008-12-21 17:13:36Z erich $
exec  mzscheme --require "$0" --main -- ${1+"$@"}
|#

#lang scheme

;; A kludge from Eli Barzilay to get the net/url library to work with
;; HTTPS
(include "eli.ss")
(require net/uri-codec)

(define *auth-url* (string->url "https://www.google.com:443/accounts/ClientLogin"))

;; Dig out a username and password from a file that happens to contain
;; that info.
(define (get-local-auth-info)
  (call-with-input-file (build-path (find-system-path 'home-dir) ".imap-authinfo")
    (lambda (ip)
      (let ((line (read-line ip)))
        (match line
          [(regexp #rx"login (.*?) password \"(.*)\"" (list _ username password))
           (values username password)])))))

(provide get-tokens)
(define (get-tokens)

  (let ((form (let-values (((email password)
                            (get-local-auth-info)))
                (string->bytes/utf-8
                 (alist->form-urlencoded
                  `((accountType . "GOOGLE")
                    (Email . ,email)
                    (Passwd . ,password)
                    (service . "cl")
                    (source . "eric.hanchrow-gcaldeduplicator-version0")))))))

    (make-immutable-hash
     (for/list ([line (in-lines (
                                 ssl:post-pure-port *auth-url*
                                 form
                                 (list "Content-type: application/x-www-form-urlencoded")))])
       (match line
         [(regexp "^([A-Za-z]+)=(.*)$" (list _ key value))
          (cons (string->symbol key) value)
          ])))))
