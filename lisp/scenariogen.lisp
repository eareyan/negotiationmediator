;
;;;
;;; enrique's scenario generator
;;;
;
#|

To create a scenario, run the following function in the lisp interpreter:

(enrique :numissues 1
         :domainsize 100
         :numconstraints 5
         :dimprobs '((1 100)) 
         :widthprobs '((1 100)))

(enrique :numissues 1
         :domainsize 10
         :numconstraints 50
         :dimprobs '((1 100)) 
         :widthprobs '((1 100)))

(enrique :numissues 2
         :domainsize 10
         :numconstraints 5
         :dimprobs '((2 50) (1 50)) 
         :widthprobs '((1 20) (2 20) (3 20) (4 20) (5 20)))

(enrique :numissues 3
         :domainsize 10
         :numconstraints 5
         :dimprobs '((1 50) (2 25) (3 25)) 
         :widthprobs '((1 20) (2 20) (3 20) (4 20) (5 20)))

numissues = number of issues in domain
domainsize = number of values for each issue 0 .. <domainsize - 1>
numconstraints = number of hypercubes
dimprobs = probability distribution for number of dimensions per hypervolume
widthprobs = probability distribution for width of a hypervolume on a given issue 

In the example above, there are:

   two issues whose value can range from 0 .. 19
   20 hypervolumes
   each hypervolume is equally likely to have one or two issues
   the hypervolumes range from 1 to 5 wide on each dimension, with equal probability

|#

(setq *random-state* (make-random-state t))

(defun gav (entity attribute) 
  "Gets the attribute value for an entity"
  (getf (rest entity) attribute))

(defun sav (entity attribute value)
  "Sets the attribute value for an entity"
  (setf (getf (rest entity) attribute) value))

(defsetf gav sav)

(defun compress (number)
  "Compresses positive integers to base 36"
    (format nil "~{~A~}"
            (reverse
             (loop with digit
                   for index from (log number 36) downto 0
                   do (multiple-value-bind (m r) (truncate number 36)
                        (setq digit r)
                        (setq number m))
                   collect (subseq "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" digit (1+ digit))))))

(defparameter *session-id* (compress (get-universal-time)))

(defun read-to-cl (arg)
  "Invokes read-from-string in common-lisp-user *package*"
  (let ((*package* (find-package 'common-lisp-user)))
    (when (stringp arg)
      (read-from-string arg nil nil))))


(defun new-id (&optional (symbol 's))
  "Creates a new id."
  (let* ((symbol (read-to-cl (format nil "~a-~a" symbol *session-id*)))
         (index (or (get symbol 'newsym-count) 0)))
    (setf (get symbol 'newsym-count) (1+ index))
    (format nil "~a-~a" symbol (1+ index))))

(defun scramble (list)
  "Scrambles the order of a list"
  (sort (copy-list list) #'(lambda (a b) (declare (ignore a b)) (zerop (random 2)))))

(defun pairs (list)
  "Returns list of all pairs of items in the list"
  (loop for i from 1 to (length list)
        nconc (loop for j from (1+ i) to (length list)
                    for v1 = (nth (1- i) list)
                    for v2 = (nth (1- j) list)
                    collect (list v1 v2))))

(defun all-issues (domain)
  "Returns the issues in a domain"
  (loop for element in domain
          append (case (first element)
                   (issue (list element))
                   (component (append (gav element :issues)
                                      (all-issues (gav element :components)))))))

(defun pick-from-list (list)
  "Picks a random item from given list"
  (when list
    (nth (random (length list)) list)))

(defun pick-from-range (min max)
  "Picks a random integer from given range"
  (+ min (random (- max min -1))))

(defun pick-weighted (probs)
  "Picks a random choice from a probability a-list"
  (when probs
    (loop with size = (loop for p in probs sum (second p))
          with threshold = (pick-from-range 1 size)
          with sum = 0 
          for prob in probs
          do (setq sum (+ sum (second prob)))
          do (when (>= sum threshold) (return (first prob))))))

(defun pick-n (n list)
  "Randomly picks N items from list"
  (loop repeat n
        for c in (scramble list)
        collect c))         

(defun renumber (domain)
  "Numbers the issues in a domain in the order they appear"
  (let ((index 0))
    (labels ((renum (elem)
               (case (first elem)
                 (issue (setf (gav elem :index) (incf index))
                        elem)
                 (component `(component :name ,(gav elem :name)
                                        :issues ,(loop for i in (gav elem :issues)
                                                   collect (renum i))
                                        :components ,(loop for next in (gav elem :components)
                                                       collect (renum next)))))))
      (loop for c in domain collect (renum c)))))


(defun create-scenario (&key (name "a scenario")
                             (description nil)
                             (numagents 2)
                             (numcomponents 1)
                             (numissues 30)
                             (domainsize 10)
                             (numconstraints 10)
                             (numshared 0)
                             (weightbias 0.6)
                             (tags nil)
                             (cpref 0) (apref 0)
                             (typeprobs '((cube 33) (bell 33) (plane 33)  (not 33)))
                             (dimprobs '((1 33) (2 33) (3 33) (4 33)))
                             (scopeprobs '((component 33) (sibling 33) (child 33)))
                             (widthprobs (loop for i from 0 to domainsize collect (list i 10))) 
                             (shapebias 0))
  (list apref cpref)
"Creates a scenario file with a hierarchical utility function.

name = name of the scenario
numcomponents = # of components
numissues = # of issues
numagents = # of agents
domainsize = size of domain for each issue
numconstraints =  # of constraints in each agents' utility function
numshared = # of constraints that are shared over all the agents. If the # is negative, the shared constraints are inverted across agents.
weightbias = how quickly constraint weights decrease with depth 
dimprobs = the probablility of different constraint dimensions
scopeprobs = % probability of different scopes of constraints (same component, sibling, child)
typeprobs = % probability for each type of constraint (cube, bell, plane)
widthprobs = % probability for different possible contraint widths
shapebias = bias towards wide trees (positive value) or narrow trees (negative value)"

  (let* ((all-issues nil) 
         (all-components nil)
         (parameters `(:numagents ,numagents
                                  :numcomponents ,numcomponents
                                  :numissues ,numissues
                                  :domainsize ,domainsize
                                  :numconstraints ,numconstraints
                                  :numshared ,numshared
                                  :weightbias ,weightbias
                                  :typeprobs ,typeprobs
                                  :dimprobs ,dimprobs
                                  :scopeprobs ,scopeprobs
                                  :widthprobs ,widthprobs
                                  :shapebias ,shapebias)))
                      
    (labels ((path (entity)
               "Finds the path for an entity"
               (gav entity :path))

             (find-component (name)
               "Finds the component with the given name"
               (find name all-components :test #'equal :key #'(lambda (c) (gav c :name))))

             (parent (component)
               "Finds the parent for the given component"
               (find-component (first (path component))))

             (siblings (component)
               "Returns the siblings for a component"
               (gav (parent component) :components))

             (depth (e)
               "Finds the depth of an entity in the component hierarchy"
               (length (path e)))

             (find-issue (index)
               "Finds issue with the given index"
               (find index all-issues :key #'(lambda (issue) (gav issue :index))))

             (add-issue (c)
               "Adds a new issue to the component"
               (let* ((cname (gav c :name))
                      (iname (format nil "~a-i~a" cname (1+ (length (gav c :issues)))))
                      (issue `(issue :type integer :name ,iname :level ,(1+ (length (gav c :path))) :from 0 :to ,(1- domainsize))))
                 (push issue all-issues)
                 (push issue (gav c :issues))))

             (create-domain ()
               "Creates a domain definition"
               (loop for cnum from 1 to numcomponents
                     for cname = (format nil "c~a" cnum)
                     for parent = (pick-weighted 
                                   (loop for c in all-components 
                                         for nk = (1+ (length (gav c :components)))
                                         for weight = (truncate (* 100 (expt nk shapebias)))
                                         collect (list c weight)))
                     for path = (when parent (cons (gav parent :name) (gav parent :path)))
                     for new = `(component :name ,cname :path ,path)
                     do (push new all-components)
                     do (when parent (push new (gav parent :components))))
               (loop for c in all-components do (add-issue c))                
               (loop repeat (- numissues numcomponents) do (add-issue (pick-from-list all-components))) 
               (renumber (last all-components)))

             (create-scale-free-constraints (numconstraints)
               "Uses preferential attachment to generate a scale-free issue network"
               (let ((constraints (loop for i from 1 to numconstraints collect `(:id ,i :issues nil)))
                     (issues (loop for i from 1 to numissues collect `(:id ,i :constraints nil))))
                 (loop for c in constraints
                   for ndim = (pick-weighted dimprobs)
                   collect (loop repeat ndim
                             for weighted = (loop for i in issues collect (list (getf i :id) (1+ (length (getf i :issues)))))
                             for issue = (pick-weighted weighted)
                             do (pushnew (getf issue :id) (getf c :issues))
                             do (pushnew (getf c :index) (getf issue :constraints))))))

             (create-constraints (numconstraints)
               (loop with constraints
                 while (< (length constraints) numconstraints)
                 for component = (pick-from-list all-components)
                 for dimension = (pick-weighted dimprobs)
                 for issues = (case (pick-weighted scopeprobs)
                                (component (pick-n dimension (gav component :issues)))
                                (sibling (loop for sib in (pick-n dimension (siblings component))
                                               collect (pick-from-list (gav sib :issues))))
                                (child (let ((child (pick-from-list (gav component :components))))
                                         (when child
                                           (list (pick-from-list (gav component :issues))
                                                 (pick-from-list (gav child :issues)))))))
                 ; do (kvp :component component :dimension dimension :issues issues)
                 do (let* ((bounds (loop for def in issues
                                     for index = (gav def :index)
                                     for width = (pick-weighted widthprobs)
                                     for min = (gav def :from)
                                     for max = (gav def :to)
                                     for lpos = (pick-from-range (- min width) max)
                                     for left = (max min lpos)
                                     for right = (min max (+ lpos width))
                                     collect `(,index :from ,left :to ,right)))
                           (weight (* (pick-from-range 1 100) (expt weightbias (1- (loop for i in issues maximize (gav i :level)))))))
                      (setq bounds (sort bounds #'< :key #'first))
                      (case (pick-weighted typeprobs)
                        (bell (push `(bell ,bounds ,weight) constraints))
                        (cube (push `(cube ,bounds ,weight) constraints))
                        (plane (push `(plane ,bounds ,weight ,(loop repeat (length bounds) collect (pick-from-range -2.0 2.0)))
                                     constraints))))
                 finally (return constraints))))
      
      (cond ((and (< numshared 0) (not (assoc 'cube typeprobs)) (not (assoc 'not typeprobs)))
             (error "To get opposed constraints, agents must have cube or not constraints"))
            ((> (- numshared) numconstraints)
             (error "You must have at least one regular constraint for every opposed constraint"))
            (t (let* ((domain (create-domain))
                      (s `(scenario :id ,(string (new-id))
                                    :name ,name
                                    :tags ,tags
                                    :description nil
                                    :domain ,domain
                                    :agents ,(loop for i from 1 to numagents
                                               collect `(agent :id ,(format nil "A~a" i)
                                                               :ufun ,(create-constraints numconstraints)))
                                    ,@parameters)))
                 (cond ((< numshared 0)
                        (loop for pair in (pairs (gav s :agents))
                          for source = (first pair)
                          for target = (second pair)
                          do (loop with count = 0
                               for original in (gav source :ufun)
                               for reverse = (case (first original)
                                               (cube `(not ,@(rest original)))
                                               (not `(cube ,@(rest original))))
                               while (< count (- numshared))
                               do (when reverse
                                    (push reverse (gav target :ufun))
                                    (incf count)))))
                       ((> numshared 0)
                        (loop with shared = (create-constraints numshared)
                          for agent in (gav s :agents)
                          do (loop for c in shared do (push c (gav agent :ufun))))))
                 (setf (gav s :description)
                       (with-output-to-string (stream)
                         (when description (format stream "<b>Description</b>: ~A<br>" description))))
                 s))))))

(defun export-negoxml (scenario file)
  "Exports scenario in the negoxml format"
  (with-open-file (stream file :direction :output :if-does-not-exist :create :if-exists :supersede)
    (let* ((domain (gav scenario :domain))
           (issues (all-issues domain)))
      (labels ((spacer (level)
                 (format nil "~{~a~}" (loop repeat (* 3 level) collect " "))))
        (format stream "<scenario id=\"~a\">" (gav scenario :id))
        (format stream "~%<domain>")
        (loop for elem in issues
          do (format stream "~%~a<issue type=\"integer\" name=\"~a\" lowerbound=\"~a\" upperbound=\"~a\"/>" 
                                  (spacer 1) (gav elem :index) (gav elem :from) (gav elem :to)))
        (format stream "~%</domain>")
        (loop for agent in (gav scenario :agents)
              do (let ()
                   (format stream "~%<profile id=\"~a\" >" (gav agent :id))
                   (format stream "~%~a<ufun\>" (spacer 1))
                   (loop for c in (gav agent :ufun)
                         for type = (first c)
                         for bounds = (second c)
                         for weight = (third c)
                         do (let ()
                              (format stream "~%~a<~a height=\"~a\">" (spacer 2) type weight)
                              (loop for i from 0
                                    for bound in bounds
                                    for index = (first bound)
                                    for min = (gav bound :from)
                                    for max = (gav bound :to)
                                    for slope = (nth i (fourth c))
                                    do (case type
                                         (plane (format stream "~% ~a<bound issue=\"~a\" min=\"~a\" max=\"~a\" slope=\"~a\"/>" (spacer 3)  index min max slope))
                                         (t (format stream "~% ~a<bound issue=\"~a\" min=\"~a\" max=\"~a\" />" (spacer 3)  index min max))))
                              (format stream "~%~a</~a>" (spacer 2) type)))
                   (format stream "~%~a</ufun>" (spacer 1))
                   (format stream "~%</profile>")))
        (format stream "~%</scenario>~%")))))

(defun enrique (&key (numissues 2) (domainsize 10) (numconstraints 20) 
                     (dimprobs '((2 50) (1 50))) (widthprobs '((1 20) (2 20) (3 20) (4 20) (5 20))))
  (let* ((s (create-scenario :numagents 2 
                           :numcomponents 1 
                           :numissues numissues 
                           :domainsize domainsize
                           :numconstraints numconstraints 
                           :dimprobs dimprobs
                           :widthprobs widthprobs
                           :scopeprobs '((component 100))
                           :typeprobs '((cube 33)))))
    (export-negoxml s (format nil "~a~a.xml" 
                              (concatenate 'string "/Users/enriqueareyan/Documents/workspace/negotiationmediator/scenarios"
                                           "/num_issues_" (write-to-string numissues) 
                                           "/domain_size_" (write-to-string domainsize)
                                           "/num_constraints_" (write-to-string numconstraints) 
                                           "/")
                              (gav s :id))) 
    (print (gav s :id)))
    (quit))
