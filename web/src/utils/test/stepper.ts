export class Stepper {
  _step: number = 0

  step(s: number) {
    expect(this._step).toBe(s - 1)
    this._step += 1
  }
}
