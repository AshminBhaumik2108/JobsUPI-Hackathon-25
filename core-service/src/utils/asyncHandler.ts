import { Request, Response, NextFunction } from "express";

type Handler = (req: Request, res: Response, next: NextFunction) => Promise<void>;

export const asyncHandler = (fn: Handler) => (req: Request, res: Response, next: NextFunction) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};
