package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Genre;

import java.util.List;
/**
 * @author Nabil L. A. @nalleon
 */
public interface IGenreRepository {
    Genre save(Genre genre);
    List<Genre> findAll();
    Genre findById(Integer id);
    Genre findByName(String name);
    boolean delete(Integer id);
    Genre update(Genre genre);
}
