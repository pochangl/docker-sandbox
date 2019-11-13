import { Model, ModelList, WebSocketModel } from '@/models'

export class Problem extends Model {
  static viewName = 'problem/problem'
  static fields = ['title', 'description', 'output_type']

  title: string
  description: string
  output_type: string // tslint:disable-line variable-name
}

export class ProblemList extends ModelList<Problem> {
  static Model = Problem
}

export class Submission extends WebSocketModel {
  static viewName = 'problem/submission'
  static fields = ['problem', 'code', 'evaluated', 'has_passed', 'stderr', 'stdout']

  problem: number = 0
  code: string = ''
  stderr: string = ''
  stdout: string = ''

  onNotification(): Promise<string> {
    return this.receive('notification')
  }

  async onResult(): Promise<Submission> {
    const data = await this.receive('result')
    const submission = new Submission()
    submission.construct(data)
    return submission
  }
}
