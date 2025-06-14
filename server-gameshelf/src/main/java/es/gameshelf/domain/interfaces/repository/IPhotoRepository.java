package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.PhotoReview;
import es.gameshelf.domain.PhotoReview;

import java.util.List;

public interface IPhotoRepository {
    PhotoReview save(PhotoReview photoReview);
    List<PhotoReview> findAll();
    PhotoReview findById(Integer id);
    PhotoReview findByName(String name);
    boolean delete(Integer id);
    PhotoReview update(PhotoReview photoReview);
}
