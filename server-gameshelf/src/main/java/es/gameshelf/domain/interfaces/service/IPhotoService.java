package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.PhotoReview;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IPhotoService {
    PhotoReview add(String name, String photo, String type);
    List<PhotoReview> findAll();
    PhotoReview findById(Integer id);
    PhotoReview findByName(String name);
    boolean delete(Integer id);
    PhotoReview update(Integer id, String name, String photo, String type);
}
