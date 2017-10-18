import { TestBed, inject } from '@angular/core/testing';

import { UsrService } from './usr.service';

describe('UsrService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [UsrService]
    });
  });

  it('should be created', inject([UsrService], (service: UsrService) => {
    expect(service).toBeTruthy();
  }));
});
