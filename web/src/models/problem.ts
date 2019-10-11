import { Model, ModelList } from '@/models'

export class Problem extends Model {
  static viewName = 'problem/problem'
  static fields = ['title', 'description']

  title: string
  description: string
}

export class ProblemList extends ModelList<Problem> {
  static Model = Problem
}

export class Submission extends Model {
  static viewName = 'problem/submission'
  static fields = ['problem', 'code', 'evaluated', 'has_passed', 'error']

  problem: number = 0
  code: string = ''
}
