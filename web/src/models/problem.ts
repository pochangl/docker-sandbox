import { Model, ModelList } from '@/models'

export class Problem extends Model {
  viewName = 'problem/problem'

  static fields = ['title', 'description']
}

export class ProblemList extends ModelList<Problem> {
  static Model = Problem
}

export class Submission extends Model {
  static fields = ['problem', 'code', 'evaluated', 'has_passed', 'error']
}
