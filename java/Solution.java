import java.util.*;

@SuppressWarnings("unchecked")
public class Solution {

  private static void solve(int numGroups, int[] students) {
    // Failing solution.  This outputs all students on the same line.
    // We need to modify this so that they are printed out in groups.
    for (int student: students) {
      System.out.print(Integer.toString(student) + " ");
    }
  }

  public static void main(String[] args) {
    // First arg is the number of groups.
    // Parse this as an int.
    int numGroups = Integer.parseInt(args[0]);

    // Second arg is comma-separated list of students' points.
    // Parse this as an array of ints.
    String[] studentStrs = args[1].split(",");
    int[] students = new int[studentStrs.length];
    for (int i = 0; i < studentStrs.length; i++) {
      students[i] = Integer.parseInt(studentStrs[i]);
    }

    solve(numGroups, students);
  }
}
