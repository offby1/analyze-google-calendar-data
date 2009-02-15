;; This will give us ssl:--- for an ssl version of url.ss, but still need an
;; explicit port number specification since url.ss does not handle that
(require scheme/unit
         net/url-sig net/url-unit
         net/tcp-sig net/tcp-unit
         net/ssl-tcp-unit)
(define-values/invoke-unit
  (compound-unit/infer (import) (export url^) (link tcp@ url@))
  (import) (export url^))
(define ssl-tcp@ (make-ssl-tcp@ #f #f #f #f #f #f #f))
(define-values/invoke-unit
  (compound-unit (import) (export URL)
    (link [((TCP : tcp^)) ssl-tcp@]
          [((URL : url^)) url@ TCP]))
  (import) (export (prefix ssl: url^)))
