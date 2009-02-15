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

;; http://code.google.com/apis/accounts/docs/AuthForInstalledApps.html
(define *auth-url* (string->url "https://www.google.com:443/accounts/ClientLogin"))

(provide get-token)
(define (get-token email password)

  (let ((form (string->bytes/utf-8
               (alist->form-urlencoded
                `((accountType . "GOOGLE")
                  (Email . ,email)
                  (Passwd . ,password)
                  (service . "cl")
                  (source . "eric.hanchrow-gcaldeduplicator-version0"))))))

    (call/ec
     (lambda (return)
       (let* ((inp (
                    ssl:post-impure-port *auth-url*
                    form
                    (list "Content-type: application/x-www-form-urlencoded")))
              (headers (purify-port inp))
              (response (read-line (open-input-string headers))))

         (match response
           [(regexp #rx"HTTP/.* 200 OK\r" (list _))

            (for ([line (in-lines inp)])
              (match line
                [(regexp "^Auth=(.*)$" (list _ token))
                 (return token)]
                [_ 'just-ignore-it]))]
           [_ (error 'get-token "bad response: ~s" headers)]
           ))))))
