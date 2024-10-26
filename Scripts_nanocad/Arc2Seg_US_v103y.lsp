;;
;; Generation de polygones reguliers sur les Arcs , Cercles et Arcs dans Polylignes 
;;
;; Les XDatas sont copiees sur la nouvelle polyligne.
;;
;; Routine:  ARC2SEG  vers 1.03 par Gilles (gile) le 10 Nov 2008
;; Transforme les arcs, cercles et polyarcs en polylignes constituees de segments droits
;;
;; 1 - Correction du bug sur les arcs > 180 degres 
;; 
;; 2  Pour les XDatas, soit je copie tout dans la nouvelle entite soit, 
;; dans le cas des polylignes avec suppression, je ne fais que modifier les sommets de la polyligne. 
;; 
;; 3 - J'ai peaufine le traitement des largeurs, si la largeur de depart et la largeur de fin different,
;; celle des segments changera aussi proportionnellement. 
;; 
;; 4 - Generation soit sur le calque courant, soit sur le calque d'origine des objets (vs 1.03)
;;

;; 
;; Minimum Translation from French to US/English 
;; 

;;
;; thx to: https://forums.autodesk.com/t5/autocad-forum/is-it-possible-to-convert-an-arc-to-a-segemented-line/m-p/5124326#M239269
;;
;; v103y: Suppressed prompt unnecessary privately
;;

(defun c:Arc2Seg (/ arc2pol pol2pol seg del org ss n ent elst)

  ;; Retourne la liste dxf de la polyligne (d'apr鑚 un arc ou un cercle)
  (defun arc2pol
	 (elst seg org / closed alpha delta cen elv rad lay nlst)
    (and (= (cdr (assoc 0 elst)) "CIRCLE") (setq closed T))
    (setq alpha	(if closed
		  (* pi 2)
		  (cdr (assoc 51 elst))
		)
	  delta	(if closed
		  (/ alpha seg)
		  (/ (ang<2pi (- alpha (cdr (assoc 50 elst)))) seg)
		)
	  cen	(cdr (assoc 10 elst))
	  elv	(caddr cen)
	  cen	(list (car cen) (cadr cen))
	  rad	(cdr (assoc 40 elst))
	  lay	(if org
		  (assoc 8 elst)
		  (cons 8 (getvar "CLAYER"))
		)
	  nlst	(vl-remove-if-not
		  (function (lambda (x) (member (car x) '(210 -3))))
		  elst
		)
	  nlst	(cons (cons 10 (polar cen alpha rad)) nlst)
    )
    (repeat (if	closed
	      (1- seg)
	      seg
	    )
      (setq
	nlst (cons (cons 10
			 (polar cen (setq alpha (- alpha delta)) rad)
		   )
		   nlst
	     )
      )
    )
    (setq nlst
	   (cons '(0 . "LWPOLYLINE")
		 (cons '(100 . "AcDbEntity")
		       (cons (cons 410 (getvar "CTAB"))
			     (cons lay
				   (cons '(100 . "AcDbPolyline")
					 (cons (cons 90
						     (if closed
						       seg
						       (1+ seg)
						     )
					       )
					       (cons (cons 70
							   (if closed
							     1
							     0
							   )
						     )
						     (cons (cons 38 elv) nlst)
					       )
					 )
				   )
			     )
		       )
		 )
	   )
    )
  )


  ;; Retourne la liste dxf de la polyligne modifi馥 (d'apr鑚 une polyligne)

  (defun pol2pol (elst	seg   org   /	  cnt	closed	    nlst  p0
		  p1	p2    bu    larg  inc	bdata delta cen	  rad
		  alpha	n
		 )
    (setq closed (logand 1 (cdr (assoc 70 elst)))
	  cnt	 0
    )
    (and (= closed 1) (setq p0 (cdr (assoc 10 elst))))
    (while elst
      (if (= (caar elst) 10)
	(progn
	  (setq	p1 (cdar elst)
		p2 (cdr (assoc 10 (cdr elst)))
		bu (cdr (assoc 42 elst))
	  )
	  (if (or (= 0 bu)
		  (and (zerop closed) (null p2))
	      )
	    (setq nlst (cons (cadddr elst)
			     (cons (caddr elst)
				   (cons (cadr elst)
					 (cons (car elst) nlst)
				   )
			     )
		       )
		  elst (cddddr elst)
	    )
	    (progn
	      (and (not p2) (= closed 1) (setq p2 p0))
	      (setq larg  (cdr (assoc 40 elst))
		    inc	  (/ (- (cdr (assoc 41 elst)) larg) seg)
		    bdata (BulgeData bu p1 p2)
		    delta (/ (car bdata) seg)
		    rad	  (abs (cadr bdata))
		    cen	  (caddr bdata)
		    alpha (angle cen p1)
		    n	  0
		    cnt	  (+ cnt seg -1)
	      )
	      (while (< n seg)
		(setq nlst (cons
			     (cons 10
				   (polar cen
					  (+ alpha (* delta n))
					  rad
				   )
			     )
			     nlst
			   )
		      nlst (cons (cons 40 larg) nlst)
		      nlst (cons (cons 41 (setq larg (+ larg inc))) nlst)
		      nlst (cons '(42 . 0.0) nlst)
		      n	   (1+ n)
		)
	      )
	      (setq elst (cddddr elst))
	    )
	  )
	)
	(setq nlst (cons (car elst) nlst)
	      elst (cdr elst)
	)
      )
    )
    (or	org
	(setq nlst (subst (cons 8 (getvar "CLAYER")) (assoc 8 nlst) nlst))
    )
    ((lambda (dxf90)
       (subst (cons 90 (+ (cdr dxf90) cnt))
	      dxf90
	      (reverse (subst '(42 . 0.0) (assoc 42 nlst) nlst))
       )
     )
      (assoc 90 nlst)
    )
  )

  ;; Fonction principale

  (or (getenv "SegmentsNumberPerCircle")
      (setenv "SegmentsNumberPerCircle" "64")
  )
  (initget 6)
  (if 

;;;;;;;;;; French version ;;;;;;;;;; 
;;    (setq seg (getint
;;		(strcat	"\nNombre de segments par arc <"
;;			(getenv "SegmentsNumberPerCircle")
;;			">: "
;;		)
;;	      )
;;    )

;;;;;;;;;; US/English version ;;;;;;;;;; 
    (setq seg (getint
		(strcat	"\nNumber of Segments per Arc <"
			(getenv "SegmentsNumberPerCircle")
			">: "
		)
	      )
    ) 
;;;;;;;;;; US/English version ;;;;;;;;;; 


     (setenv "SegmentsNumberPerCircle" (itoa seg))
     (setq seg (atoi (getenv "SegmentsNumberPerCircle")))
  ) 


;;;;;;;;;; French version ;;;;;;;;;; 
;;  (initget "Oui Non")
;;  (if (= "Oui"
;;	 (getkword "\nEffacer les objets source [Oui/Non] ? <N>: ")
;;      )
;;    (setq del T)
;;  )

;;;;;;;;;; US/English version ;;;;;;;;;; 
;  (initget "Yes No")
;  (if (= "Yes"
;	 (getkword "\nErase Source Objects [Yes/No] ? <N>: ")
;      )
;    (setq del T)
;  )
;
  (setq del T)

;;;;;;;;;; US/English version ;;;;;;;;;; 

;;;;;;;;;; French version ;;;;;;;;;;
;;  (initget "Courant Origine")
;;  (if (= "Origine"
;;	 (getkword
;;	   "\nCalque des nouveaux objets [Courant/Origine] ? <C>: "
;;	 )
;;      )
;;    (setq org T)
;;  ) 

;;;;;;;;;; US/English version ;;;;;;;;;; 
;  (initget "Current Original")
;  (if (= "Original"
;	 (getkword
;	   "\nLayer for NEW Objects [Current/Original] ? <C>: "
;	 )
;      )
;    (setq org T)
;  ) 
;
  (setq org T)

;;;;;;;;;; US/English version ;;;;;;;;;; 

;;;;;;;;;; French version ;;;;;;;;;;
;;  (prompt
;;    "\nS駘ectionner les objets ・traiter ou <tous>."
;;  ) 

;;;;;;;;;; US/English version ;;;;;;;;;; 
  (prompt
    "\nSelect Objects or <all>."
  ) 




  (and
    (or	(setq ss (ssget '((0 . "ARC,CIRCLE,LWPOLYLINE"))))
	(setq ss (ssget "_X" '((0 . "ARC,CIRCLE,LWPOLYLINE"))))
    )
    (setq n 0)
    (while (setq ent (ssname ss n))
      (setq elst (entget ent '("*")))
      (if (= (cdr (assoc 0 elst)) "LWPOLYLINE")
	((if del
	   entmod
	   entmake
	 )	   (pol2pol elst seg org)
	)
	(progn
	  (entmake (arc2pol elst seg org))
	  (and del (entdel ent))
	)
      )
      (setq n (1+ n))
    )
  )
  (princ)
)


;; BulgeData
;; Retourne les donn馥s d'un polyarc (angle rayon centre) 

(defun BulgeData (bu p1 p2 / alpha rad cen)
  (setq	alpha (* 2 (atan bu))
	rad   (/ (distance p1 p2)
		 (* 2 (sin alpha))
	      )
	cen   (polar p1
		     (+ (angle p1 p2) (- (/ pi 2) alpha))
		     rad
	      )
  )
  (list (* alpha 2.0) rad cen)
)

;;; Ang<2pi
;;; Retourne l'angle, ・2*k*pi pr鑚, compris entre 0 et 2*pi

(defun ang<2pi (ang)
  (if (and (<= 0 ang) (< ang (* 2 pi)))
    ang
    (ang<2pi (rem (+ ang (* 2 pi)) (* 2 pi)))
  )
)
