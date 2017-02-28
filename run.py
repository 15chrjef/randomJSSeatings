#!/usr/bin/python
import argparse, math, os.path, random, sys, subprocess
from re import split

def mean(nums):
  return 1.0 * sum(nums) / len(nums)

def std(nums):
  avg = 1.0 * mean(nums)
  return math.sqrt(mean([math.pow(num - avg, 2) for num in nums]))

class InputGenerator():
  def __init__(self, groups, students, minimum, maximum, skew):
    self.groups = groups
    self.students = students
    self.minimum = minimum
    self.maximum = maximum
    self.skew = skew

  def random(self):
    seed = (1 - math.pow(random.random(), self.skew))
    return int(math.floor((seed * (self.maximum - self.minimum)) + self.minimum))

  def generate(self):
    students = [self.random() for student in xrange(0, self.students)]
    students.sort()
    return {"groups": self.groups, "students": students}

class Runner():
  def __init__(self, generator, script, should_eval):
    self.generator = generator
    self.script = script
    self.should_eval = should_eval

  def run(self):
    self.input = self.generator.generate()
    self.output = self.exec_script()
    if self.should_eval:
      self.evaluation = self.evaluate()
      return self.evaluation
    else:
      return None

  def print_results(self):
    print ""
    print "Groups:"
    print self.input["groups"]
    print ""
    print "Students:"
    print str(self.input["students"])[1:-1]
    print ""
    print "Output:"
    print self.output
    if self.should_eval and hasattr(self, "evaluation"):
      print "Group averages: %s" % str(self.evaluation["averages"])[1:-1]
      print "Standard deviation of group averages: %f" % self.evaluation["score"]
    print ""

  def exec_script(self):
    subprocess.call(["chmod", "+x", self.script])
    
    groupsStr = str(self.input["groups"])
    studentsStr = ",".join([str(student) for student in self.input["students"]])
    
    args = ["./"+self.script]
    args.append(groupsStr)
    args.append(studentsStr)
    return subprocess.check_output(args)

  def evaluate(self):
    input = self.input
    output = self.output

    lines = [line.strip() for line in output.strip().split("\n") if bool(line.strip())]
    groups = [[int(student) for student in split("[\s,]", line)] for line in lines]

    if input["groups"] != len(groups):
      raise ValueError("Expected %d groups, but got %d" % (input["groups"], len(groups)))

    total_students = sum([len(group) for group in groups])
    if len(input["students"]) != total_students:
      raise ValueError("Expected %d students, but got %d" % (len(input["students"]), total_students))

    maxStudentsInGroup = max([len(group) for group in groups])
    minStudentsInGroup = min([len(group) for group in groups])
    if maxStudentsInGroup - minStudentsInGroup > 1:
      raise ValueError("Groups were not of similar sizes, one had %d students and one had %d students"
                  % (minStudentsInGroup, maxStudentsInGroup))

    grouped_students = [student for group in groups for student in group]
    diff = list(set(input["students"]) - set(grouped_students))
    if len(diff) > 0:
      raise ValueError("Original list of students differ from result")

    averages = [mean(group) for group in groups]
    return {"averages": averages, "score" : std(averages)}

def parser():
  parser = argparse.ArgumentParser(description="Seating chart verifier")
  parser.add_argument("script", type=str, help="Your script file")

  parser.add_argument("-s", "--students", type=int, default=24,
                      help="set number of students")
  parser.add_argument("-g", "--groups", type=int, default=6,
                      help="set number of groups")
  parser.add_argument("-n", "--min", type=int, default=-50,
                      help="set min point value")
  parser.add_argument("-m", "--max", type=int, default=250,
                      help="set max point value")
  parser.add_argument("-k", "--skew", type=int, default=1,
                      help="skew the distribution (pass a value between -3 and 3)")
  parser.add_argument("-l", "--log", action="store_true", default=False,
                      help="log your solution without evaluating it")
  parser.add_argument("-r", "--repetitions", type=int,  default=1,
                      help="run n trials and average your scores")
  return parser

def main():
  args = parser().parse_args()

  if not os.path.exists(args.script):
    sys.stderr.writelines("No script found at \"%s\"." % args.script)
    return 1

  if args.students <= 0 or args.groups <= 0:
    sys.stderr.writelines("Student and group counts must be great than 0.")
    return 1

  if args.min >= args.max:
    sys.stderr.writelines("Max must be greater than min.")
    return 1

  if args.repetitions < 1:
    sys.stderr.writelines("Repetitions must be a positive integer.")
    return 1

  generator = InputGenerator(args.groups, args.students, args.min, args.max, args.skew)
  runner = Runner(generator, args.script, not args.log)
  if args.repetitions == 1:
    try:
      runner.run()
      runner.print_results()
    except ValueError as e:
      sys.stderr.writelines("Unable to process output: " + str(e) + "\n")
      return 1
    return 0
  else:
    all_stds = []
    for i in xrange(args.repetitions):
      result = runner.run()
      all_stds.append(result["score"])
    print "After %d runs, the average of all scores is %f" % (args.repetitions, mean(all_stds))
    return 0

if __name__ == "__main__":
  status = main()
  sys.exit(status)
